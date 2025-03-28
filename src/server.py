import serial
import asyncio
import json
import threading

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()

# CORS settings
origins = ["http://127.0.0.1:5500", "http://localhost:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared data container
latest_data = {"heart_rate": "--", "spo2": "--"}

# Read serial data in background thread
def read_serial_data():
    global latest_data
    try:
        ser = serial.Serial("COM11", 115200, timeout=1) #input your COM port
        while True:
            line = ser.readline().decode().strip()
            if line and "," in line:
                hr, spo2 = line.split(",")
                latest_data = {"heart_rate": hr, "spo2": spo2}
    except serial.SerialException as e:
        print(f"[Serial Error] {e}")
    except Exception as e:
        print(f"[Read Error] {e}")

# Start background thread
serial_thread = threading.Thread(target=read_serial_data, daemon=True)
serial_thread.start()

# WebSocket route
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text(json.dumps(latest_data))
            await asyncio.sleep(1)  # Send data every second
    except Exception as e:
        print(f"[WebSocket Error] {e}")
    finally:
        await websocket.close()
