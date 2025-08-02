# TCP Socket Implementation

This project contains a complete TCP socket server and client implementation in Python.

## Files

- `server.py` - TCP server that can handle multiple client connections
- `client.py` - TCP client that can connect to the server and send messages
- `README.md` - This documentation file

## Features

### Server Features
- Multi-threaded server that can handle multiple clients simultaneously
- Echo functionality (sends back received messages)
- Proper error handling and connection cleanup
- Graceful shutdown with Ctrl+C
- Configurable host and port

### Client Features
- Interactive mode for sending messages
- Test mode for automated testing
- Automatic message listening in background thread
- Proper connection management and error handling

## Usage

### Starting the Server

1. **Default settings** (localhost:8888):
   ```bash
   python server.py
   ```

2. **Custom host and port**:
   ```bash
   python server.py 0.0.0.0 9999
   ```

### Using the Client

1. **Interactive mode** (default):
   ```bash
   python client.py
   ```
   - Type messages and press Enter to send
   - Type 'quit' to exit

2. **Custom server address**:
   ```bash
   python client.py 192.168.1.100 9999
   ```

3. **Test mode** (automated testing):
   ```bash
   python client.py 127.0.0.1 8888 test
   ```

## Example Session

### Terminal 1 (Server)
```bash
$ python server.py
TCP Server started on 127.0.0.1:8888
Waiting for client connections...
New connection from ('127.0.0.1', 54321)
Received from ('127.0.0.1', 54321): Hello, server!
Received from ('127.0.0.1', 54321): How are you?
Connection closed for ('127.0.0.1', 54321)
```

### Terminal 2 (Client)
```bash
$ python client.py
Connected to server at 127.0.0.1:8888
Type messages to send to server (type 'quit' to exit):
> Hello, server!
Server: Server received: Hello, server!
> How are you?
Server: Server received: How are you?
> quit
Disconnected from server
```

## Network Configuration

- **Default Host**: `127.0.0.1` (localhost)
- **Default Port**: `8888`
- **Protocol**: TCP (reliable, connection-oriented)
- **Socket Type**: `SOCK_STREAM`

## Error Handling

The implementation includes comprehensive error handling for:
- Connection failures
- Network timeouts
- Invalid addresses
- Socket errors
- Graceful shutdown

## Threading

- Server uses threading to handle multiple clients simultaneously
- Each client connection runs in its own thread
- Client uses threading for background message listening

## Security Notes

- This is a basic implementation for learning purposes
- No authentication or encryption
- Not suitable for production use without additional security measures
- Consider using SSL/TLS for secure communications in production

## Troubleshooting

1. **Port already in use**: Change the port number or wait for the previous process to finish
2. **Connection refused**: Make sure the server is running before starting the client
3. **Permission denied**: Try using a port number above 1024 or run with appropriate permissions 