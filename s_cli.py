import socket
import ssl
import threading
import os

HOST = '127.0.0.1'
PORT = 65432

def receive(sock):
    while True:
        try:
            header = sock.recv(1024).decode()
            if not header:
                break

            parts = header.split('|')
            if parts[0] == 'MSG':
                print(f"{parts[1]}: {'|'.join(parts[2:])}")
            elif parts[0] == 'FILE':
                sender, filename, filesize = parts[1], parts[2], int(parts[3])
                print(f"\nReceiving file '{filename}' ({filesize} bytes) from {sender}...")

                with open(f"received_from_{sender}_{filename}", 'wb') as f:
                    total = 0
                    while total < filesize:
                        chunk = sock.recv(min(4096, filesize - total))
                        if not chunk:
                            break
                        f.write(chunk)
                        total += len(chunk)
                print(f"File saved as 'received_from_{sender}_{filename}'\n")
        except:
            break

def send(sock, username):
    while True:
        try:
            msg = input()
            if msg.lower() == 'exit':
                break
            elif msg.startswith('/file '):
                _, path = msg.split(' ', 1)
                if not os.path.exists(path):
                    print("File not found.")
                    continue
                filesize = os.path.getsize(path)
                filename = os.path.basename(path)
                sock.sendall(f"FILE|{filename}|{filesize}".encode())
                with open(path, 'rb') as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        sock.sendall(chunk)
                print(f"Sent file '{filename}' to all.")
            else:
                sock.sendall(f"MSG|{username}|{msg}".encode())
        except:
            break
    sock.close()

def main():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # برای تست، اعتبارسنجی گواهی را غیرفعال می‌کنیم

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            username_prompt = ssock.recv(1024).decode()
            if username_prompt.startswith("USERNAME:"):
                username = input("Enter your username: ")
                ssock.sendall(username.encode())

                threading.Thread(target=receive, args=(ssock,), daemon=True).start()
                send(ssock, username)

main()
