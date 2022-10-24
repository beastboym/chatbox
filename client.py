import socket

host = "127.0.0.1"
port = 6007

# déclarer un socket
client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

client.connect((host, port))

nom = input("quel est votre nom :")
while True:
    msg = input(f"{nom} : ")
    msg = msg.encode("utf-8")
    client.send(msg)

    server_recv = client.recv(150)
    server_recv = server_recv.decode("utf-8")
    print(server_recv)
