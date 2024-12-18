import socket
import os
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
import struct
import binascii


class ImageReceiverApp:
    def __init__(self, root):
        self.port = 8888
        self.root = root
        self.root.title("AMB82-MINI Image Receiver")
        self.root.geometry("600x400")

//With the next line, modify to add your custom path to receive the images
        self.save_path = r"C:\AMB82_Captures"
        os.makedirs(self.save_path, exist_ok=True)

        self.create_widgets()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)

        threading.Thread(target=self.start_server, daemon=True).start()

    def create_widgets(self):
        self.log_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=20)
        self.log_display.pack(padx=10, pady=10)
        self.status_label = tk.Label(self.root, text=f"Listening on port {self.port}", fg="green")
        self.status_label.pack(pady=5)

    def log_message(self, message):
        self.root.after(0, self._log_message, message)

    def _log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_display.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_display.see(tk.END)

    def receive_bytes(self, sock, size):
        """Receive exactly size bytes."""
        data = bytearray()
        while len(data) < size:
            chunk = sock.recv(min(size - len(data), 4096))
            if not chunk:
                raise ConnectionError("Connection closed prematurely")
            data.extend(chunk)
        return bytes(data)

    def hex_dump(self, data, max_bytes=32):
        """Create a hex dump of the data for debugging."""
        return binascii.hexlify(data[:max_bytes]).decode()

    def handle_client(self, client_socket, address):
        try:
            # Set a timeout for receiving data
            client_socket.settimeout(10.0)

            # First, try to receive just one byte to see what we're getting
            initial_data = client_socket.recv(1)
            self.log_message(f"First byte received: {self.hex_dump(initial_data)}")

            # Read the rest of the size data (assuming 4 bytes total)
            size_bytes = initial_data + self.receive_bytes(client_socket, 3)
            self.log_message(f"Size bytes received (hex): {self.hex_dump(size_bytes)}")

            # Convert size bytes to integer using big-endian format
            img_size = struct.unpack('>I', size_bytes)[0]
            self.log_message(f"Decoded image size: {img_size} bytes")

            # Sanity check the size
            if img_size <= 0 or img_size > 10_000_000:  # Max 10MB
                raise ValueError(f"Invalid image size: {img_size}")

            # Receive image data
            self.log_message(f"Starting to receive {img_size} bytes of image data...")
            img_data = self.receive_bytes(client_socket, img_size)

            # Log the first few bytes of the image
            self.log_message(f"First bytes of image data: {self.hex_dump(img_data[:16])}")

            # Verify JPEG header
            if img_data.startswith(b'\xFF\xD8'):
                self.log_message("Valid JPEG header detected")
            else:
                self.log_message(f"Warning: Invalid JPEG header. First bytes: {self.hex_dump(img_data[:4])}")

            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.save_path, f"capture_{timestamp}.jpg")

            with open(filename, 'wb') as f:
                f.write(img_data)

            self.log_message(f"Saved image: {filename} ({len(img_data)} bytes)")

        except ConnectionError as e:
            self.log_message(f"Connection error with {address}: {e}")
        except struct.error as e:
            self.log_message(f"Error parsing size from {address}: {e}")
        except Exception as e:
            self.log_message(f"Error handling client {address}: {e}")
            import traceback
            self.log_message(traceback.format_exc())
        finally:
            try:
                client_socket.close()
            except:
                pass

    def start_server(self):
        self.log_message("Server started")
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                self.log_message(f"Connection from {address[0]}")
                threading.Thread(target=self.handle_client,
                                 args=(client_socket, address),
                                 daemon=True).start()
            except Exception as e:
                self.log_message(f"Server error: {e}")


def main():
    root = tk.Tk()
    app = ImageReceiverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()