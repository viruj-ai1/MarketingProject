import os
import sys
import socket

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'

# Change working directory to synthesis_route_finder directory
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')

    local_ip = get_local_ip()
    print(f"\nSynthesis Route Finder App starting...")
    print(f"Local access:   http://127.0.0.1:{port}")
    print(f"LAN access:     http://{local_ip}:{port}\n")

    app.run(debug=False, host=host, port=port)
