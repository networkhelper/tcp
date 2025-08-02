import socket

host = "127.0.0.1"
port = 12345

try:
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        message = "hello server"
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"received from server: {data.decode()}")

except ConnectionRefusedError:
    print(f"connection refused by the server {host}:{port}")
except Exception as e:
    print(f"an error occurred: {e}")