import json
import socket
import threading
from time import sleep


class UDPSender:
    def __init__(self, host='127.0.0.1', port=50000, print_msgs=False):
        self.print_msgs = print_msgs
        self.send_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        """Send Udp data to the specified send address

        Args:
            data (Any): Any data you want to send over Udp
        """
        try:
            # Serialize the data to JSON format
            message = json.dumps(data)
            self.sock.sendto(message.encode(), self.send_address)
            if self.print_msgs: print(f"Sent: {data}")
        except Exception as e:
            if self.print_msgs: print(f"Error sending data: {e}")

    def stop(self):
        self.sock.close()


class UDPReceiver:
    def __init__(self, host='127.0.0.1', port=50001, print_msgs=False, tuning_mode=None):
        self.print_msgs = print_msgs
        self.receive_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.receive_address)
        self.running = True
        self.messages = []
        self.candidate_keys = []
        self.tuning_mode = tuning_mode

    def listen(self):
        """Listen for Udp messages sent to the receive address"""
        while self.running:
            try:
                # Set a timeout to avoid blocking indefinitely while waiting for data
                self.sock.settimeout(1)
                try:
                    # Wait for incoming data
                    data, _ = self.sock.recvfrom(4096)

                    # Deserialize the data from JSON format
                    data = json.loads(data.decode())
                    if self.print_msgs: print(f"Received: {data}")
                    if isinstance(data, dict):
                        try:
                            tuning_mode = data["tuning_mode"]
                            if tuning_mode in [None, "static", "dynamic"]:
                                self.tuning_mode = tuning_mode
                        except:
                            print("exception")
                    elif data and any(isinstance(item, str) for item in data):
                        self.candidate_keys = data
                    elif data and any(isinstance(item, list) for item in data):
                        self.messages = data
                    

                except socket.timeout:
                    # If no data is received within the timeout, just loop again
                    continue
            except json.JSONDecodeError:
                if self.print_msgs: print("Error: Received invalid JSON data.")
            except socket.error as e:
                if self.print_msgs: print(f"Socket error: {e}")
                self.running = False
            except Exception as e:
                if self.print_msgs: print(f"Unexpected error receiving data: {e}")
                self.running = False

    def start_listener(self):
        # Daemonize the listener thread so it closes with the main program
        listener_thread = threading.Thread(target=self.listen)
        listener_thread.daemon = True
        listener_thread.start()

    def stop(self):
        self.running = False
        self.sock.close()


# Example usage:
if __name__ == "__main__":
    # Example of starting a receiver
    receiver = UDPReceiver(host='127.0.0.1', port=50000, print_msgs=True)
    receiver.start_listener()

    # Example of starting a sender
    sender = UDPSender(host='127.0.0.1', port=50000, print_msgs=True)

    # Example loop to send messages
    try:
        while True:
            # Example data to send
            data = [[1, 2, 3], [4, 5, 6]]
            sender.send(data)
            sleep(3)
    except KeyboardInterrupt:
        sender.stop()
        receiver.stop()
