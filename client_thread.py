import socket
import threading

HOST = '127.0.0.1'
PORT = 8888
EXIT_COMMAND = 'exit'

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message.lower() == EXIT_COMMAND:
                print("Server ended the chat.")
                break
            print(f"Server: {message}")
        except:
            break

def send_messages(sock):
    while True:
        try:
            message = input("You: ")
            sock.sendall(message.encode())
            if message.lower() == EXIT_COMMAND:
                break
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((HOST, PORT))
        print("Connected to the server.")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()
    except ConnectionRefusedError:
        print("Unable to connect to the server.")
    finally:
        client_socket.close()
        print("Connection closed.")
