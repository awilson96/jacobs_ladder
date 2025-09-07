import json
import socket
import threading
from time import sleep
from abc import ABC, abstractmethod


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

    def send_bytes(self, data_bytes: bytes):
        """Send raw bytes to the Dart app

        Args:
            data_bytes (bytes): header bitmask pair for dart app
        """
        try:
            self.sock.sendto(data_bytes, self.send_address)
            if self.print_msgs:
                print(f"Sent bytes: {data_bytes}")
        except Exception as e:
            if self.print_msgs:
                print(f"Error sending data: {e}")

    def stop(self):
        self.sock.close()

class UDPReceiver(ABC):
    def __init__(self, host='127.0.0.1', port=50001, print_msgs=False):
        self.print_msgs = print_msgs
        self.receive_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.receive_address)
        self.running = True

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
                    if self.print_msgs: 
                        print(f"Received: {data}")
                        
                    self.dispact_message(data=data)

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
        self.listener_thread = threading.Thread(target=self.listen)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def stop(self):
        self.running = False
        self.listener_thread.join()
        self.sock.close()
    
    @abstractmethod
    def dispact_message(self, data):
        """This is a method which parses messages across a user specified UDP interface

        Args:
            data (Any): any data the user wishes to send over UDP
        """
        pass


# Example usage:
if __name__ == "__main__":
    # Example of starting a receiver
    class CustomUDPReceiver(UDPReceiver):
        def dispact_message(self, data):
            """Process list of lists message types

            Args:
                data (list[list]): only process data which is an instance of list[list]
            """
            if isinstance(data, list) and isinstance(data[0], list):
                print("printing list of lists")
                for sublist in data:
                    for number in sublist:
                        print(number)
    receiver = CustomUDPReceiver(host='127.0.0.1', port=50000, print_msgs=True)
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
        print("Exiting...")
        sender.stop()
        receiver.stop()
        
