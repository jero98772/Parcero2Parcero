# Parcero2Parcero_browser
(in process)



## How to Run


1. Start the Tracker Server: Run the tracker server code on a known IP address (e.g., a local network IP).
2. Replace TRACKER_SERVER_IP in the peer code with the tracker’s IP.
3. Run the peer client code on multiple devices or instances.

	pip install fastapi uvicorn jinja2

	uvicorn main:app --host 0.0.0.0 --port 9609 


## TODO 

peer must show files depending of directory

multiples trackers

upgrade client.py and peer.py to poo