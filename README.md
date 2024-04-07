# Protobuf-encoded Logger Simulator

## Project Overview

This project includes a client-server architecture where the client sends protobuf-encoded, length-prefixed log messages to the server over TCP. The server is designed to handle these messages from up to 100 concurrent connections, processing and logging the messages to standard output. This setup mimics a real-world scenario of distributed logging with considerations for network unreliability and message serialization.

## Getting Started

To get started with this project, you'll need to have Python 3.10 or newer and Poetry installed on your system for dependency management.

### Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**

    First, clone the project repository to your local machine:

    ```bash
    git clone https://github.com/thiagogenez/protobuf-logger-app.git
    ```

    Replace `https://github.com/thiagogenez/protobuf-logger-app.git` with the actual URL of the repository.

2. **Install Dependencies**

    Navigate to the project directory and use Poetry to install the necessary dependencies:

    ```bash
    cd protobuf-logger-app
    poetry install --no-dev
    ```

### Running the Applications

It's recommended to run each application in its own terminal window for clarity and ease of monitoring. Here's how to get each application up and running:

#### Logger App (Server)

1. **Open a new terminal window** for the Logger App.

2. **Start the server** by running the following command:

    ```bash
    poetry run logger-app
    ```

    This command initiates the server, which will listen for and process incoming log messages on `127.0.0.1:15000`.

3. **To exit** the Logger App, use `CTRL+C` in its terminal window. This will shut down the server.

#### Naive Client App

1. **Open another new terminal window** for the Naive Client App.

2. **Run the client** application with the following command:

    ```bash
    poetry run naive-client-app
    ```

    This starts the client, which then connects to the server and begins transmitting log messages.

3. **To exit** the Naive Client App, similarly use `CTRL+C` in its terminal window.

