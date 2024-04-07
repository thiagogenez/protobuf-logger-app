"""
This module defines a Logger server class that listens for incoming connections
and processes log messages sent by clients. Messages are expected to be protobuf-encoded.
"""

import socket
import threading
import struct
import logging
from . import log_message_pb2 as proto

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class Logger:
    """
    A Logger server class that listens on a specified host and port for incoming log messages,
    decodes them from protobuf, and logs the contents o.
    """
    def __init__(self, host="127.0.0.1", port=15000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """Starts the TCP server to listen for incoming connections."""

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(100)  # Listen for up to 100 concurrent connections
        logging.info(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_sock, address = self.server_socket.accept()
                logging.info(f"Accepted connection from {address}")
                client_thread = threading.Thread(
                    target=self.handle_client_connection, args=(client_sock,)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            logging.info("Server shutting down.")
        finally:
            self.server_socket.close()

    def handle_client_connection(self, client_socket):
        """Handles incoming client connections and processes messages."""
        try:
            while True:
                # Read message length first
                raw_msglen = client_socket.recv(4)
                if not raw_msglen:
                    break
                msglen = struct.unpack(">L", raw_msglen)[0]

                # Read the message data
                data = b""
                while len(data) < msglen:
                    packet = client_socket.recv(msglen - len(data))
                    if not packet:
                        return
                    data += packet

                # Deserialize the data to a LogMessage object
                # pylint: disable=no-member
                log_message = proto.LogMessage()
                log_message.ParseFromString(data)

                # Convert MAC bytes to a readable format
                mac_address = ":".join(f"{byte:02x}" for byte in log_message.mac)

                # Log the message to stdout
                log_msg = (
                    f"{log_message.log_level} - {log_message.logger} - "
                    f"{mac_address} - {log_message.message}"
                )
                logging.info(log_msg)
        finally:
            client_socket.close()


def main():
    """Main function that initializes and starts the Logger server."""
    server = Logger()
    server.start()


if __name__ == "__main__":
    main()
