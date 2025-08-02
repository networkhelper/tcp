import socket
import threading


host = "127.0.0.1"
port = 8888
EXIT_COMMAND = "exit"


def receive_message(conn):
    while True:
        try:
            message = conn.recv(1024).decode()
            if message == EXIT_COMMAND:
                print("Client disconnected")
                break
            print(f"\n Received message: {message}")
        except:
            break


def send_message(conn):
     while True:
        try:
                message = input("Enter message: ")
                conn.sendall(message.encode())
                if message.lower() == EXIT_COMMAND:
                    break
        except:
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"server listening on {host}:{port}")
    
    conn, addr = server_socket.accept()
    print(f"connected by {addr}")
    
    receive_thread = threading.Thread(target=receive_message, args=(conn,))
    send_thread = threading.Thread(target=send_message, args=(conn,))
    
    receive_thread.start()
    send_thread.start()
    
    receive_thread.join()
    send_thread.join()
    conn.close()
    print("connection closed.")
    