import socket, pickle
from Crypto.Cipher import DES
from secrets import token_bytes
import random


host = "127.0.0.1"
port = 6007

# déclarer un socket
client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect((host, port))

# Algorithme deffie hellman
g = random.randint(500, 9556891747)
str_key = str(g)
client.send(str_key.encode())
key = client.recv(500)
p = int(key.decode("utf-8"))
bob = random.randint(500, p - 1)
alice = g ^ bob % p
client.send(str(alice).encode())
server_key = client.recv(500)
g = int(server_key.decode("utf-8"))
cle_commune = (g ^ bob % p).to_bytes(8, "big")


def encrypt(msg):
    cipher = DES.new(cle_commune, DES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode("ascii"))
    return nonce, ciphertext, tag


def decrypt(nonce, ciphertext, tag):
    cipher = DES.new(cle_commune, DES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode("ascii")
    except:
        print("Le message n'est pas fiable")
        raise SystemExit


while True:
    try:
        msg = input("client : ")
        msg_obj = pickle.dumps(encrypt(msg))
        client.send(msg_obj)
        server_recv = client.recv(500)
        nonce, cipher, tag = pickle.loads(server_recv)
        server_recv = decrypt(nonce, cipher, tag)
        print("server: ", server_recv)
    except KeyboardInterrupt:
        print("fermer")
        raise SystemExit
