# backend/app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store EEG data
SAVE_DIR = "saved_eeg"
os.makedirs(SAVE_DIR, exist_ok=True)

# Store live connections
active_connections = []


@app.websocket("/ws/eeg")
async def websocket_endpoint(websocket: WebSocket):
    """Handles live EEG data from the simulator."""
    await websocket.accept()
    active_connections.append(websocket)
    print("🔌 EEG WebSocket connected")

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_eeg.jsonl")
    filepath = os.path.join(SAVE_DIR, filename)

    try:
        with open(filepath, "a") as f:
            while True:
                data = await websocket.receive_text()
                msg = json.loads(data)
                f.write(json.dumps(msg) + "\n")
                f.flush()
    except WebSocketDisconnect:
        print("❌ EEG WebSocket disconnected")
        active_connections.remove(websocket)
    except Exception as e:
        print("⚠️ Error:", e)
        if websocket in active_connections:
            active_connections.remove(websocket)


@app.get("/replay")
def list_saved_files():
    """List all saved EEG data files."""
    files = sorted(os.listdir(SAVE_DIR))
    return {"files": files}


@app.get("/replay/{filename}")
def get_saved_data(filename: str):
    """Return saved EEG data for replay visualization."""
    filepath = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(filepath):
        return {"error": "File not found"}
    with open(filepath) as f:
        data = [json.loads(line) for line in f]
    return {"data": data}


@app.get("/")
def root():
    return {"message": "EEG Backend Active"}
