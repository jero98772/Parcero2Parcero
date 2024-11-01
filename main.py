from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import threading
from peer import start_tracker
from client import request_file,get_peer_list, get_file_list,start_peer_server,register_with_tracker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Global variable to hold the peer list
list_peers = []

@app.on_event("startup")
async def startup_event():
    global list_peers
    # Start the tracker in a separate thread
    threading.Thread(target=start_tracker).start()
    # Start the client in a separate thread
    threading.Thread(target=start_peer_server).start()
    register_with_tracker()

@app.on_event("shutdown")
async def shutdown_event():
    global tracker_socket
    if tracker_socket:
        try:
            tracker_socket.close()  # Close the tracker socket
            print("Tracker socket closed.")
        except Exception as e:
            print(f"Error closing tracker socket: {e}")
    # Add any other cleanup logic as necessary

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    global list_peers
    # Get the current list of peers
    list_peers = get_peer_list()
    
    return templates.TemplateResponse("index.html", {"request": request, "peers": list_peers})

@app.get("/files/{peer_ip}", response_class=HTMLResponse)
async def list_files(peer_ip: str, request: Request):
    # Get the list of files from the specified peer
    files = get_file_list(peer_ip)
    return templates.TemplateResponse("files.html", {"request": request, "files": files, "peer_ip": peer_ip})

@app.get("/{peer_ip}/{file_name}", response_class=HTMLResponse)
async def render(peer_ip: str, file_name: str, request: Request):
    # Request the file from the peer and retrieve its content
    request_file(peer_ip, file_name)

    return templates.TemplateResponse(file_name, {"request": request})

@app.get("/config", response_class=HTMLResponse)
async def config(request: Request):
    return templates.TemplateResponse("config.html", {"request": request, "peers": list_peers})