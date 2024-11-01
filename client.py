import socket
import threading
import os

PEER_PORT = 5000
BUFFER_SIZE = 4096
TRACKER_IP = "192.168.0.18"  # Replace with the tracker's IP address
TRACKER_PORT = 6000
SHARED_FOLDER = "templates"

# Ensure the shared folder exists
os.makedirs(SHARED_FOLDER, exist_ok=True)

def register_with_tracker():
    """
    Registers this peer with the tracker server.
    """
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.connect((TRACKER_IP, TRACKER_PORT))
    tracker_socket.send("REGISTER".encode())
    response = tracker_socket.recv(BUFFER_SIZE).decode()
    print(response)
    tracker_socket.close()

def get_peer_list():
    """
    Gets the list of peers from the tracker.
    """
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.connect((TRACKER_IP, TRACKER_PORT))
    tracker_socket.send("GET_PEERS".encode())
    peers = tracker_socket.recv(BUFFER_SIZE).decode().splitlines()
    tracker_socket.close()
    return peers

def start_peer_server():
    """
    Starts a server to listen for file requests and file list requests from other peers.
    """
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.bind(("0.0.0.0", PEER_PORT))
    peer_socket.listen(5)
    print(f"Peer server started on port {PEER_PORT}")

    while True:
        client_socket, addr = peer_socket.accept()
        threading.Thread(target=handle_file_request, args=(client_socket,)).start()

def handle_file_request(client_socket):
    """
    Handles requests from other peers for either file download or file list.
    """
    try:
        request_type = client_socket.recv(BUFFER_SIZE).decode()
        
        if request_type == "LIST_FILES":
            # Send list of files in shared folder
            file_list = "\n".join(os.listdir(SHARED_FOLDER))
            client_socket.send(file_list.encode())
        
        elif request_type == "REQUEST_FILE":
            # Send a requested file
            file_name = client_socket.recv(BUFFER_SIZE).decode()
            file_path = os.path.join(SHARED_FOLDER, file_name)
            
            if os.path.exists(file_path):
                client_socket.send("OK".encode())
                with open(file_path, "rb") as file:
                    while (chunk := file.read(BUFFER_SIZE)):
                        client_socket.send(chunk)
                print(f"Sent {file_name}")
            else:
                client_socket.send("FILE_NOT_FOUND".encode())
    except Exception as e:
        print(f"Error sending file or file list: {e}")
    finally:
        client_socket.close()

def get_file_list(peer_ip):
    """
    Requests the list of available files from another peer.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, PEER_PORT))
    client_socket.send("LIST_FILES".encode())
    
    file_list = client_socket.recv(BUFFER_SIZE).decode().splitlines()
    client_socket.close()
    print(f"Files available from {peer_ip}: {file_list}")
    return file_list

def request_file(peer_ip, file_name):
    """
    Requests a file from another peer.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, PEER_PORT))
    client_socket.send("REQUEST_FILE".encode())
    client_socket.send(file_name.encode())
    
    response = client_socket.recv(BUFFER_SIZE).decode()
    if response == "OK":
        with open(os.path.join(SHARED_FOLDER, file_name), "wb") as file:
            while True:
                chunk = client_socket.recv(BUFFER_SIZE)
                if not chunk:
                    break
                file.write(chunk)
        print(f"Downloaded {file_name} from {peer_ip}")
    else:
        print(f"{file_name} not found on peer {peer_ip}")
    client_socket.close()

