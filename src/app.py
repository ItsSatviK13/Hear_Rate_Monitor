from flask import Flask, jsonify
import serial
import time

app = Flask(__name__)

ser = serial.Serial("COM3", 115200, timeout=1)  # Change COM3 if needed
time.sleep(2)

@app.route('/data', methods=['GET'])
def get_data():
    ser.flush()
    line = ser.readline().decode("utf-8").strip()
    if line:
        try:
            bpm, spo2 = map(int, line.split(","))
            return jsonify({"bpm": bpm, "spo2": spo2})
        except ValueError:
            return jsonify({"error": "Invalid data"}), 500
    return jsonify({"error": "No data"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
