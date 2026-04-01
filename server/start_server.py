import socket
import subprocess
import os

def get_free_port():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

if __name__ == "__main__":
    dynamic_port = get_free_port()
    print(f"🚀 [LearnMate Service] Dynamically resolved free port: {dynamic_port}")
    
    # Export it to Vite's local environment overrides instantly
    env_path = os.path.join(os.path.dirname(__file__), "..", "client", ".env.local")
    
    # Ensure client dir exists, though it already does
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    
    with open(env_path, "w") as f:
        f.write(f"VITE_BACKEND_PORT={dynamic_port}\n")
    
    print(f"🔗 [LearnMate Service] Shared dynamic port with Vite frontend via {env_path}")
    
    # Launch Uvicorn with the dynamically found port
    subprocess.run(["uvicorn", "src.main:app", "--reload", "--port", str(dynamic_port)])
