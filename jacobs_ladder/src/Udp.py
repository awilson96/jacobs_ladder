import logging 
import json
import socket
import threading
from time import sleep
from abc import ABC, abstractmethod

from .Logging import setup_logging


class UDPSender:
    def __init__(self, host: str, port: int, logger: logging.Logger):
        self.logger = logger
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
            self.logger.debug(f"Sent: {data}")
        except Exception as e:
            self.logger.error(f"Error sending data: {e}")

    def send_bytes(self, data_bytes: bytes):
        """Send raw bytes to the Dart app

        Args:
            data_bytes (bytes): header bitmask pair for dart app
        """
        try:
            self.sock.sendto(data_bytes, self.send_address)
            self.logger.debug(f"Sent bytes: {data_bytes}")
        except Exception as e:
            self.logger.debug(f"Error sending data: {e}")

    def stop(self):
        self.sock.close()

class UDPReceiver(ABC):
    def __init__(self, host: str, port: int, logger: logging.Logger):
        self.logger = logger
        self.receive_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.receive_address)
        self.running = True

    def listen(self):
        """Listen for UDP messages sent to the receive address."""
        while self.running:
            try:
                # Set a timeout so the loop can exit cleanly
                self.sock.settimeout(1)
                try:
                    # Wait for incoming data (up to 4 KB)
                    data, _ = self.sock.recvfrom(4096)
                    self.logger.debug(f"Received raw UDP data: {data.hex()}")
                    self.dispatch_message(data=data)

                except socket.timeout:
                    # If no data within timeout, loop again
                    continue

            except socket.error as e:
                self.logger.error(f"Socket error: {e}")
                self.running = False
            except Exception as e:
                self.logger.error(f"Unexpected error receiving data: {e}")
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
    def dispatch_message(self, data):
        """This is a method which parses messages across a user specified UDP interface

        Args:
            data (Any): any data the user wishes to send over UDP
        """
        pass


# Example usage:
if __name__ == "__main__":
    logger = setup_logging("ExampleUdpLogs")
    # Example of starting a receiver
    class CustomUDPReceiver(UDPReceiver):
        def dispatch_message(self, data):
            """Process list of lists message types

            Args:
                data (list[list]): only process data which is an instance of list[list]
            """
            if isinstance(data, list) and isinstance(data[0], list):
                self.logger.info("printing list of lists")
                for sublist in data:
                    for number in sublist:
                        self.logger.info(number)
    receiver = CustomUDPReceiver(host='127.0.0.1', port=50000, logger=logger)
    receiver.start_listener()

    # Example of starting a sender
    sender = UDPSender(host='127.0.0.1', port=50000, logger=logger)

    # Example loop to send messages
    try:
        while True:
            # Example data to send
            data = [[1, 2, 3], [4, 5, 6]]
            sender.send(data)
            sleep(3)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sender.stop()
        receiver.stop()
        
