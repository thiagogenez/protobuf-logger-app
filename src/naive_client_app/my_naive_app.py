import socket
import struct
import logging
from typing import List, Tuple
from . import log_message_pb2 as proto
import time

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def create_log_message(log_level: str, logger: str, mac: List[int], message: str) -> bytes:
    """
    Creates a serialized log message ready to be sent over the network.
    """
    # Validate MAC address format
    if not all(0 <= byte <= 255 for byte in mac):
        raise ValueError("MAC address bytes must be in the range 0-255")
    
    lm = proto.LogMessage()
    lm.log_level = log_level
    lm.logger = logger
    lm.mac = bytes(mac)
    lm.message = message

    # Serialize the LogMessage to a string
    payload = lm.SerializeToString()

    # Prefix each message (payload) with a 4-byte length (network byte order)
    return struct.pack('>L', len(payload)) + payload

def send_messages(host: str, port: int, messages: List[Tuple[str, str, List[int], str]]):
    """
    Connects to the server and sends multiple messages with arbitrary pauses between them.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            logging.info("Connected to %s:%s", host, port)

            for log_level, logger, mac, message in messages:
                try:
                    msg = create_log_message(log_level, logger, mac, message)
                    sock.sendall(msg)
                    logging.info("Log message sent: %s", message)
                    # Arbitrary pause, for demonstration you can adjust the sleep time
                    time.sleep(2)
                except Exception as e:
                    logging.error("Error sending message: %s", e)
                    break  

    except socket.error as e:
        logging.error("Socket error: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)

def main():
    host = '127.0.0.1'
    port = 15000
    
    # Define multiple messages to be sent
    messages = [
        ('ERROR', 'main', [0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff], 'First test message'),
        ('INFO', 'main', [0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff], 'Second test message'),
        # Add more messages as needed
    ]

    send_messages(host, port, messages)

if __name__ == '__main__':
    main()
