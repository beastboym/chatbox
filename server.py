import socket

host = "127.0.0.1"
port = 6007

# déclarer un socket
server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# identifier le socket en server
server.bind((host, port))
server.listen(1)

# attend une connexion
client, ip = server.accept()
print("connexion etablie avec : ", ip)

while True:
    client_recv = client.recv(150)
    # décoder le message en utf-8
    client_recv = client_recv.decode("utf-8")
    print(client_recv)
    # si le message est vide on ferme
    if not client_recv:
        print("fermer")
        break
    msg = input("->")
    msg = msg.encode("utf-8")
    client.send(msg)

client.close()
socket.close()
