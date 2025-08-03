import socket
import ssl
import threading
import os

HOST = '127.0.0.1'
PORT = 65432
CERT_FILE = 'cert/server.crt'
KEY_FILE = 'cert/server.key'

clients = {}
lock = threading.Lock()

def broadcast(message, sender_sock=None):
    with lock:
        for client in clients:
            if client != sender_sock:
                try:
                    client.sendall(message.encode())
                except:
                    client.close()
                    del clients[client]

def broadcast_file(sender, filename, filesize, sender_sock):
    with lock:
        receivers = [c for c in clients if c != sender_sock]

    # ارسال header
    for r in receivers:
        try:
            r.sendall(f"FILE|{sender}|{filename}|{filesize}".encode())
        except:
            pass

    # ارسال فایل به همه
    total = 0
    while total < int(filesize):
        chunk = sender_sock.recv(min(4096, int(filesize) - total))
        if not chunk:
            break
        for r in receivers:
            try:
                r.sendall(chunk)
            except:
                pass
        total += len(chunk)

def handle_client(conn):
    try:
        conn.sendall("USERNAME:".encode())
        username = conn.recv(1024).decode().strip()
        with lock:
            clients[conn] = username
        broadcast(f"MSG|SERVER|{username} joined the chat.", conn)

        while True:
            header = conn.recv(1024).decode()
            if not header:
                break

            parts = header.split('|')

            if parts[0] == 'MSG':
                sender, msg = parts[1], '|'.join(parts[2:])
                broadcast(f"MSG|{sender}|{msg}", conn)
            elif parts[0] == 'FILE':
                _, filename, filesize = parts
                broadcast_file(username, filename, filesize, conn)

    except Exception as e:
        print("Client error:", e)
    finally:
        with lock:
            if conn in clients:
                left_user = clients[conn]
                del clients[conn]
                broadcast(f"MSG|SERVER|{left_user} left the chat.")
        conn.close()

def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"🔐 Secure Server listening on {HOST}:{PORT}...")

        while True:
            client_sock, addr = sock.accept()
            ssl_sock = context.wrap_socket(client_sock, server_side=True)
            threading.Thread(target=handle_client, args=(ssl_sock,), daemon=True).start()

start_server()
