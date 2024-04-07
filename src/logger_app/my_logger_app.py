import socket
import threading
from . import log_message_pb2 as proto
import struct
import sys


def handle_client_connection(client_socket):
    while True:
        # Read message length first
        raw_msglen = client_socket.recv(4)
        if not raw_msglen:
            break  # No more data from client
        msglen = struct.unpack(">L", raw_msglen)[0]

        # Read the message data
        data = b""
        while len(data) < msglen:
            packet = client_socket.recv(msglen - len(data))
            if not packet:
                return  # Connection closed
            data += packet

        # Deserialize the data to a LogMessage object
        log_message = proto.LogMessage()
        log_message.ParseFromString(data)

        # Convert MAC bytes to a readable format
        mac_address = ":".join(f"{byte:02x}" for byte in log_message.mac)

        # For demonstration, log the message to stdout
        print(
            f"{log_message.log_level} - {log_message.logger} - {mac_address} - {log_message.message}"
        )


def start_server(host="127.0.0.1", port=15000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(100)  # Listen for up to 100 concurrent connections

    print("Server listening on port", port)

    try:
        while True:
            client_sock, address = server_socket.accept()
            print(f"Accepted connection from {address}")
            client_thread = threading.Thread(target=handle_client_connection, args=(client_sock,))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()


def main():
    start_server()


if __name__ == "__main__":
    main()
