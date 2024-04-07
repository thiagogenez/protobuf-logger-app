import socket
import struct
import logging
import time
import random
from typing import List
from datetime import datetime
from . import log_message_pb2 as proto  # type: ignore[attr-defined]


# Configuration
HOST = "127.0.0.1"
PORT = 15000
LOG_FORMAT = "%(asctime)s - %(message)s"

# Setup basic logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class MyNaiveApp:
    def __init__(self, host: str, port: int):
        """Initializes the application with the specified host address and port number."""
        self.host = host
        self.port = port

    def _create_log_message(
        self, log_level: str, logger: str, mac: List[int], message: str
    ) -> bytes:
        """Creates a serialized protobuf-encoded, length-prefixed message."""

        lm = proto.LogMessage()
        lm.log_level = log_level
        lm.logger = logger
        lm.mac = bytes(mac)
        lm.message = message
        payload = lm.SerializeToString()
        return struct.pack(">L", len(payload)) + payload

    def _generate_random_mac(self) -> List[int]:
        """Generate a random MAC address."""

        return [random.randint(0, 255) for _ in range(6)]

    def _generate_random_message(self) -> tuple[str, str]:
        """Generates a message with a current timestamp, log level, and content."""

        messages_with_codes = [
            ("System startup complete.", "INFO", "100"),
            ("User logged in.", "INFO", "101"),
            ("Error reading configuration file.", "ERROR", "200"),
            ("Database connection successful.", "INFO", "102"),
            ("File not found.", "ERROR", "201"),
            ("Data processing completed.", "INFO", "103"),
            ("Network connection lost.", "ERROR", "202"),
            ("Out of memory.", "ERROR", "203"),
            ("User request timed out.", "WARNING", "300"),
            ("New user account created.", "INFO", "104"),
            ("Security update applied.", "INFO", "105"),
            ("Unexpected input format received.", "ERROR", "204"),
            ("Backup completed successfully.", "INFO", "106"),
            ("License verification failed.", "ERROR", "205"),
            ("Disk space reaching capacity.", "WARNING", "301"),
            ("New device detected.", "INFO", "107"),
            ("Service started.", "INFO", "108"),
            ("Service stopped.", "WARNING", "302"),
            ("Password change required.", "INFO", "109"),
            ("High CPU usage detected.", "WARNING", "303"),
            ("Low battery warning.", "WARNING", "304"),
            ("New connection established.", "INFO", "110"),
            ("Session expired.", "WARNING", "305"),
            ("Configuration updated.", "INFO", "111"),
            ("Device disconnected.", "WARNING", "306"),
            ("Firmware upgrade required.", "INFO", "112"),
            ("Temperature threshold exceeded.", "WARNING", "307"),
            ("Data synchronization started.", "INFO", "113"),
            ("Data synchronization completed.", "INFO", "114"),
            ("Invalid login attempt.", "ERROR", "206"),
            ("", "INFO", ""),
        ]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        message, level, code = random.choice(messages_with_codes)
        formatted_message = f"{current_time} - {message}"
        return level, formatted_message

    def send_multiple_messages(self):
        """Connects to the server and sends multiple random messages indefinitely.

        This function manages connection attempts and reconnections, and logs messages sent. It also
        handles user interruptions for graceful shutdown.
        """
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.host, self.port))
                    logging.info(f"Connected to {self.host}:{self.port}")

                    while True:
                        mac = self._generate_random_mac()
                        log_level, message = self._generate_random_message()
                        msg = self._create_log_message(log_level, "main", mac, message)
                        sock.sendall(msg)
                        logging.info(f"Sent: {message}")
                        time.sleep(random.uniform(0.5, 2))
                    break  # Exit the loop after sending the messages
            except socket.error as e:
                # Wait a bit before trying to reconnect
                logging.error(f"Socket error: {e}, attempting to reconnect...")
                time.sleep(5)
            except KeyboardInterrupt:
                logging.info("Shutdown signal received, stopping...")
                break
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                break


def main():
    sender = MyNaiveApp(HOST, PORT)
    sender.send_multiple_messages()


if __name__ == "__main__":
    main()
