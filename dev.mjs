import { spawn, execSync } from 'child_process';
import net from 'net';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 1. Load .env variables (User prefers it in server/.env)
const envPath = path.join(__dirname, 'server', '.env');
let envContent = '';
try {
  envContent = fs.readFileSync(envPath, 'utf-8');
} catch (e) {
  // If .env doesn't exist, we'll use defaults
}

const envVars = {};
for (const line of envContent.split('\n')) {
  const match = line.match(/^\s*([^#=]+)\s*=\s*(.*)/);
  if (match) {
    envVars[match[1].trim()] = match[2].trim();
  }
}

const FRONTEND_BASE_PORT = parseInt(envVars.FRONTEND_PORT || '5200', 10);
const BACKEND_BASE_PORT = parseInt(envVars.BACKEND_PORT || '8200', 10);

// 2. Function to find the next available port sequentially
async function findFreePort(basePort) {
  let port = basePort;
  while (port < basePort + 100) {
    const isFree = await new Promise((resolve) => {
      const server = net.createServer();
      server.listen(port, () => {
        server.once('close', () => resolve(true));
        server.close();
      });
      server.on('error', () => resolve(false));
    });
    if (isFree) return port;
    port++;
  }
  throw new Error(`Could not find a free port starting from ${basePort}`);
}

// 3. Function to gracefully detect and forcibly kill the process holding a port
function killPort(port) {
  try {
    const pids = execSync(`lsof -ti:${port}`).toString().trim().split('\n');
    for (const pid of pids) {
      if (pid) {
        console.log(`[Cleanup] Forcibly killing process ${pid} on port ${port}...`);
        try {
            process.kill(parseInt(pid, 10), 'SIGKILL');
        } catch (killErr) {
            // Process might've already exited
        }
      }
    }
  } catch (e) {
    // Port not in use or lsof command failed/nothing to parse, ignore
  }
}

async function start() {
  const frontendPort = await findFreePort(FRONTEND_BASE_PORT);
  const backendPort = await findFreePort(BACKEND_BASE_PORT);

  console.log(`🚀 [Dev Orchestrator] Frontend assigned to port: ${frontendPort}`);
  console.log(`🚀 [Dev Orchestrator] Backend assigned to port:  ${backendPort}`);

  // Write variables natively into the localized .env file so Vite picks it up
  const clientEnvPath = path.join(__dirname, 'client', '.env.local');
  fs.writeFileSync(clientEnvPath, `VITE_BACKEND_PORT=${backendPort}\n`);
  console.log(`🔗 [Dev Orchestrator] Updated ${clientEnvPath} with backend port ${backendPort}`);

  // Launch Frontend
  const feProcess = spawn('npm', ['run', 'dev', '--', '--port', frontendPort.toString(), '--strictPort'], {
    cwd: path.join(__dirname, 'client'),
    stdio: 'inherit',
    env: { ...process.env, ...envVars }
  });

  // Launch Backend
  const beProcess = spawn('uvicorn', ['src.main:app', '--reload', '--port', backendPort.toString()], {
    cwd: path.join(__dirname, 'server'),
    stdio: 'inherit',
    // Inject the dynamically found frontend port to backend if it needs to know it
    env: { ...process.env, ...envVars, DYNAMIC_FRONTEND_URL: `http://localhost:${frontendPort}` }
  });

  // 4. Force Cleanup on Exit (Ctrl+C)
  const cleanup = () => {
    console.log('\n🛑 [Dev Orchestrator] Shutting down servers and force-cleaning ports...');
    
    feProcess.kill('SIGINT');
    beProcess.kill('SIGINT');

    // Make absolutely sure the ports are free for next time to prevent hanging services
    setTimeout(() => {
        killPort(frontendPort);
        killPort(backendPort);
        process.exit(0);
    }, 500); // give them half a second to gracefully terminate before sending SIGKILL
  };

  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
}

start().catch(err => {
  console.error(err);
  process.exit(1);
});
