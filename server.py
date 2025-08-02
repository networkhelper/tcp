import socket

host = "127.0.0.1"
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"server is listening on {host}:{port}")
    
    conn, addr = server_socket.accept()
    with conn:
        print(f"connected by {addr}")
        data = conn.recv(1024)
        if data:
            print(f"received from client: {data.decode()}")
            response = "hello client"
            conn.sendall(response.encode())
            
