# Import the generated classes
from . import schema_pb2


def create_log_message():
    # Create an instance of LogMessage
    log_message = schema_pb2.LogMessage()

    # Set the fields
    log_message.log_level = "INFO"
    log_message.logger = "ExampleLogger"
    log_message.mac = b"\x00\x0A\x95\x9D\x68\x16"  # Example MAC address in bytes
    log_message.message = "This is a test log message."

    return log_message


def main():
    # Create a log message
    log_msg = create_log_message()

    # Serialize the message to a byte string
    serialized_msg = log_msg.SerializeToString()
    print("Serialized message:", serialized_msg)

    # Deserialize the byte string back into a LogMessage object
    new_log_msg = schema_pb2.LogMessage()
    new_log_msg.ParseFromString(serialized_msg)
    print("Deserialized message:")
    print("Log Level:", new_log_msg.log_level)
    print("Logger:", new_log_msg.logger)
    print("MAC:", new_log_msg.mac)
    print("Message:", new_log_msg.message)


if __name__ == "__main__":
    main()
