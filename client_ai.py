import socket
import sys
import threading
import time

class TCPClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
    
    def connect(self):
        """Connect to the TCP server"""
        try:
            # Create socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            
            print(f"Connected to server at {self.host}:{self.port}")
            return True
            
        except socket.error as e:
            print(f"Connection failed: {e}")
            return False
    
    def send_message(self, message):
        """Send a message to the server"""
        if not self.connected:
            print("Not connected to server")
            return False
        
        try:
            # Send message
            self.client_socket.send(message.encode('utf-8'))
            return True
        except socket.error as e:
            print(f"Error sending message: {e}")
            self.connected = False
            return False
    
    def receive_message(self):
        """Receive a message from the server"""
        if not self.connected:
            return None
        
        try:
            # Receive data
            data = self.client_socket.recv(1024)
            if data:
                return data.decode('utf-8')
            else:
                self.connected = False
                return None
        except socket.error as e:
            print(f"Error receiving message: {e}")
            self.connected = False
            return None
    
    def listen_for_messages(self):
        """Listen for incoming messages from server"""
        while self.connected:
            message = self.receive_message()
            if message:
                print(f"Server: {message}")
            else:
                break
        print("Disconnected from server")
    
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        print("Disconnected from server")

def interactive_client():
    """Interactive client that allows user to send messages"""
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8888
    
    client = TCPClient(host, port)
    
    if not client.connect():
        return
    
    # Start listening thread
    listen_thread = threading.Thread(target=client.listen_for_messages)
    listen_thread.daemon = True
    listen_thread.start()
    
    try:
        print("Type messages to send to server (type 'quit' to exit):")
        while client.connected:
            message = input("> ")
            if message.lower() == 'quit':
                break
            
            if not client.send_message(message):
                break
                
    except KeyboardInterrupt:
        print("\nShutting down client...")
    finally:
        client.disconnect()

def test_client():
    """Simple test client that sends a few messages"""
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8888
    
    client = TCPClient(host, port)
    
    if not client.connect():
        return
    
    # Send test messages
    test_messages = [
        "Hello, server!",
        "This is a test message",
        "How are you doing?",
        "Goodbye!"
    ]
    
    for message in test_messages:
        print(f"Sending: {message}")
        if client.send_message(message):
            # Wait for response
            response = client.receive_message()
            if response:
                print(f"Received: {response}")
            time.sleep(1)
        else:
            break
    
    client.disconnect()

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[3] == "test":
        test_client()
    else:
        interactive_client() 