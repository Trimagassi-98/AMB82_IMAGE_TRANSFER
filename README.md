# AMB82_IMAGE_TRANSFER
A custom TCP socket-based communication to transfer image data from the Arduino (AMB82-MINI) to a Python-based server.

# Overview

The system consists of:

Arduino Code: Captures images using a camera module, compresses them, and uploads them to a server over WiFi.

Python Code: Acts as a server to receive, process, and save the transmitted images.

# Features
Wireless image capture and transfer.
Automatic image saving with timestamped filenames.
GUI-based logging for easy monitoring.

System Requirements
Hardware
AMB82-MINI microcontroller with camera module.
WiFi network.
Host computer to run the Python receiver.

Software
Arduino IDE with necessary libraries (e.g., WiFi, VideoStream).
Python 3.9+ with required modules:
socket
threading
tkinter

# Setup Instructions

-- Arduino Setup
Open the Arduino IDE.
Install required libraries using the Library Manager:
WiFi
VideoStream
Load the provided Arduino sketch.

Update the WiFi credentials in the code:

# char ssid[] = "YOUR_SSID";    // Replace with your network SSID
# char pass[] = "YOUR_PASSWORD"; // Replace with your network password

Update the server IP and port if needed:

# #define SERVER_IP "192.168.10.20"
# #define SERVER_PORT 8888

Upload the sketch to the AMB82-MINI.

# Python Setup

Install Python 3.9+ on your computer.

Install required libraries:
pip install tkinter
Save the provided Python script to your computer.

Update the save path if needed:
self.save_path = r"C:\Your\Preferred\Directory"

Run the script:

python image_receiver.py

# Usage

Power on the AMB82-MINI and ensure it connects to your WiFi network.
Start the Python script on your host computer.
The Python GUI will display logs of incoming connections and image transfers.
Captured images will be saved in the specified directory with timestamped filenames.

# Troubleshooting

Common Issues
 -- Arduino not connecting to WiFi:
Double-check WiFi credentials.
Ensure the server IP matches the host computer's IP.

 -- Python script not receiving data:
Verify that the port (default: 8888) is open and not blocked by a firewall.
Ensure the AMB82-MINI is correctly configured to send data to the host's IP.

# Challenges and Known Issues
-- Unsupported File Format:
The images successfully upload to the server, but the resulting files are in an unsupported or corrupted format.
Possible Cause: This might be due to incorrect encoding or an incomplete image data transfer




