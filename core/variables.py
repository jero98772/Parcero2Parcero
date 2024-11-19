import socket

def get_host_ip():
    """
    Get the host's IP address automatically.
    Returns:
        str: The IP address of the host.
    """
    try:
        # Create a socket to connect to a public server to determine the host IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Connect to a public DNS server
            host_ip = s.getsockname()[0]
        return host_ip
    except Exception as e:
        return f"Error retrieving IP: {e}"



BUFFER_SIZE = 4096
TRACKER_PORT = 6000
PEER_PORT = 5000
TRACKER_IP = get_host_ip()#"192.168.0.12"  # Replace with the tracker's IP address
SHARED_FOLDER = "templates"
TRACKERS_FILE="data/trackers.txt"
peer_list = []
