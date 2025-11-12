# 🧠 Smart EEG Fatigue Detection System

![3D Brain](https://cdn3d.iconscout.com/3d/premium/thumb/brain-3d-icon-download-in-png-blend-fbx-gltf-file-formats--human-medical-healthcare-medicine-anatomy-pack-science-icons-5792545.png?f=webp&w=120)  
_A cutting-edge project combining real-time EEG data streaming, fatigue analysis, and visualization._

---

## 🚀 Overview

**Smart EEG Fatigue Detection System** is a modern full-stack application that simulates, streams, and analyzes EEG brainwave data.  
It enables **live plotting**, **data logging**, and **offline playback** for performance tracking and fatigue detection — designed for researchers, developers, and students exploring **NeuroTech + AI**.

---

## 🧩 Features

- 🔌 **Real-time EEG Data Simulation**  
  Generates synthetic EEG signals using an asynchronous simulator.

- 📡 **Live WebSocket Streaming**  
  Uses FastAPI + WebSockets for real-time bidirectional data exchange.

- 📈 **Live Plot Visualization**  
  Displays continuous brainwave graph updates using Matplotlib.

- 💾 **Automatic Data Logging**  
  Saves EEG samples locally in `.csv` format for later analysis.

- 🔁 **Offline Replay Mode**  
  Replay and visualize previously recorded EEG sessions anytime.

- ⚡ **FastAPI Backend API**  
  Handles data input/output, model integration, and session management.

- 🧠 **Fatigue Detection Logic (extendable)**  
  Ready to plug in ML/AI models for real fatigue state prediction.

---

## 🧬 Tech Stack

| Layer | Tools & Libraries |
|-------|-------------------|
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Realtime** | WebSockets |
| **Simulator** | Python AsyncIO, Matplotlib |
| **Data Handling** | CSV, JSON |
| **Frontend (optional)** | React / Streamlit (extendable) |
| **Visualization** | Matplotlib, Numpy |
| **Deployment** | Docker, GitHub Actions (planned) |

---

## 🧠 System Architecture

```mermaid
flowchart LR
A[EEG Simulator 🧩] -->|WebSocket| B(FastAPI Backend ⚙️)
B --> C[(Database / CSV Logger 💾)]
B --> D[Visualization / Dashboard 📊]
D --> E[User 🧍‍♂️]
