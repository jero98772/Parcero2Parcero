import socket
import threading
from core.variables import *


def handle_peer(connection, address):
    """
    Handles each peer's connection to register or request the list of peers.
    """
    try:
        action = connection.recv(BUFFER_SIZE).decode()
        
        if action == "REGISTER":
            # Register the peer
            peer_list.append(address[0])
            print(f"Registered peer: {address[0]}")
            connection.send("Registered successfully".encode())
        
        elif action == "GET_PEERS":
            # Send the list of peers
            peers = "\n".join(peer_list)
            connection.send(peers.encode())
        
    except Exception as e:
        print(f"Error handling peer {address}: {e}")
    finally:
        connection.close()

def start_tracker():
    """
    Starts the tracker server to listen for peer connections.
    """
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.bind(("0.0.0.0", TRACKER_PORT))
    tracker_socket.listen(10)
    print(f"Tracker server started on port {TRACKER_PORT}")

    while True:
        conn, addr = tracker_socket.accept()
        threading.Thread(target=handle_peer, args=(conn, addr)).start()

#if __name__ == "__main__":
#    start_tracker()

