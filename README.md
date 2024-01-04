# BetterDiscord
This is a simple chat application implemented in Python using the Pygame library for the client-side and Python's built-in socket library for the server-side. The application allows users to connect to a server and exchange messages in real-time.

## Prerequisites
 - Python 3.x
 - Pygame library (install via `pip install pygame`)

## Getting Started
### Server Setup
 1. Open server.py and configure the SERVER_HOST and SERVER_PORT variables to match your server's IP address and desired port.
 2. Run server.py to start the server.

### Client Setup
 1. Open client.py and set the SERVER_HOST and SERVER_PORT variables to match the server's IP address and port.
 2. Run client.py to start the client application.

### Features
 - Real-time chat with a server
 - Dynamic resizing of the client window
 - Separate chat, input, channels, and members sections
