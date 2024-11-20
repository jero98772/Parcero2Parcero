# Parcero2Parcero Distributed Webserver

**Parcero2Parcero** is a distributed web server application that allows peers to share and retrieve files through a tracker-based system. The system includes a tracker server and peer clients, working together to facilitate Distrubuted file sharing and communication.

inspirated in [beakerbrowser](https://beakerbrowser.com/)

## Features

- A tracker server to manage peer registration and maintain a list of active peers.
- Peer clients that can:
  - Register with the tracker.
  - Share their available files.
  - Request and retrieve files from other peers.

- A web-based interface to:
  - View connected peers.
  - List files available from a specific peer.
  - Request and download files.
  - View Html websites of others in your browser directly

---

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- Pip package manager

### Step 1: Install Required Dependencies

Run the following command to install the necessary Python libraries:

```bash
pip install fastapi uvicorn jinja2
```

---

## How to Run

### 1. Start the Tracker Server
The tracker server is integrated into the application. It manages the list of active peers. Follow these steps to launch it:

1. Run the application using the command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 9609
   ```

2. The tracker server will start on the specified host and port.

3. Ensure that `TRACKER_SERVER_IP` in the configuration matches the IP address of the tracker server.

### 2. Start Peer Clients
Peers are independent entities that register with the tracker and share files. Start the peer clients as follows:

1. Ensure the peer code has the correct `TRACKER_SERVER_IP`.
2. Run the application using the same command as above.

---

## Usage

### Access the Web Interface

1. Open a browser and navigate to:
   ```
   http://<TRACKER_SERVER_IP>:9609/
   ```

2. You will see the main dashboard listing all connected peers.


3. Add yours html files for share in template folder
---

## Routes

### Tracker Dashboard
- **`GET /`**  
  Displays the list of connected peers and their details.

### File Listing
- **`GET /files/{peer_ip}`**  
  Lists the files shared by a specific peer.

### File Retrieval
- **`GET /{peer_ip}/{file_name}`**  
  Requests and downloads a file from the specified peer.

### Configuration
- **`GET /config`**  
  Displays the tracker and peer configuration settings.

---

## Shutdown

To stop the application:
1. Use `Ctrl+C` to terminate the running application.
2. Ensure sockets and threads are closed properly. The application will automatically handle the cleanup process.

---

## Future Improvements (In Progress)
- Enhanced peer authentication and security.
- Support for peer-to-peer communication without a central tracker.
- Improved UI for file previews and transfers.

---

Enjoy decentralized file sharing with **Parcero2Parcero**!
