import asyncio
import json
import random
import time
import threading
import websockets
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os

BACKEND_URL = "ws://localhost:8000/ws/eeg"
CSV_FILE = "eeg_data.csv"

NUM_CHANNELS = 8
SAMPLE_INTERVAL = 0.2  # seconds

# --- Shared data ---
data_buffer = []
max_points = 100
x_data = list(range(max_points))
y_data = [[0]*max_points for _ in range(NUM_CHANNELS)]

# --- Prepare output CSV ---
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["timestamp"] + [f"ch_{i+1}" for i in range(NUM_CHANNELS)]).to_csv(CSV_FILE, index=False)

# --- Setup Matplotlib ---
plt.style.use("seaborn-v0_8-darkgrid")
fig, ax = plt.subplots(figsize=(10, 6))
lines = [ax.plot([], [], label=f"Ch {i+1}")[0] for i in range(NUM_CHANNELS)]
ax.set_xlim(0, max_points)
ax.set_ylim(-100, 100)
ax.set_title("🧠 Live EEG Simulation")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude (µV)")
ax.legend(loc="upper right")

# --- Data generation ---
def generate_fake_eeg():
    return [round(random.uniform(-80, 80), 2) for _ in range(NUM_CHANNELS)]

async def send_data():
    """Connect to backend and stream data."""
    while True:
        try:
            async with websockets.connect(BACKEND_URL) as ws:
                print(f"✅ Connected to backend {BACKEND_URL}")
                while True:
                    eeg_data = generate_fake_eeg()
                    payload = {"timestamp": time.time(), "eeg_data": eeg_data}
                    await ws.send(json.dumps(payload))

                    # Save locally
                    df = pd.DataFrame([[payload["timestamp"]] + eeg_data],
                                      columns=["timestamp"] + [f"ch_{i+1}" for i in range(NUM_CHANNELS)])
                    df.to_csv(CSV_FILE, mode='a', header=False, index=False)

                    # Update live buffer
                    data_buffer.append(eeg_data)
                    if len(data_buffer) > max_points:
                        data_buffer.pop(0)

                    await asyncio.sleep(SAMPLE_INTERVAL)
        except Exception as e:
            print(f"⚠️ Connection error: {e}. Retrying in 3s...")
            await asyncio.sleep(3)

def run_sender():
    """Start async loop in a background thread."""
    asyncio.run(send_data())

# --- Animation update ---
def update_plot(_):
    if not data_buffer:
        return lines
    latest_data = data_buffer[-1]
    for i in range(NUM_CHANNELS):
        y_data[i].append(latest_data[i])
        if len(y_data[i]) > max_points:
            y_data[i].pop(0)
        lines[i].set_data(x_data, y_data[i])
    return lines

# --- Main ---
if __name__ == "__main__":
    sender_thread = threading.Thread(target=run_sender, daemon=True)
    sender_thread.start()

    ani = animation.FuncAnimation(fig, update_plot, blit=True, interval=200, cache_frame_data=False)
    print("🎬 Live EEG graph started. Close window to stop.")
    plt.show()
    print("🛑 Simulation stopped.")
