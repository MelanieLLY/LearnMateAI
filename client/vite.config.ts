import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load variables from .env / .env.local to access VITE_BACKEND_PORT
  const env = loadEnv(mode, process.cwd(), '');
  const targetHost = `http://127.0.0.1:${env.VITE_BACKEND_PORT || 8000}`;

  return {
    plugins: [tailwindcss(), react()],
    server: {
      proxy: {
        '/api': {
          target: targetHost,
          changeOrigin: true,
        },
        '/uploads': {
          target: targetHost,
          changeOrigin: true,
        }
      }
    }
  }
})
