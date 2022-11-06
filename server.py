import random
import socket, pickle
from Crypto.Cipher import DES
from secrets import token_bytes


host = "127.0.0.1"
port = 6007


# déclarer un socket
server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# identifier le socket en server
server.bind((host, port))
server.listen(1)

# attend une connexion
client, ip = server.accept()

# Algorithme deffie hellman
p = 9576890767  # Nombre premier arbitraire (public)
alice = random.randint(500, p - 1)  # nombre arbitraire inférieur à p-1
# recevoir le premier nombre pour l'etablissement de clé
key = client.recv(500)
g = int(key.decode("utf-8"))
# envoyer notre chiffre de depart
str_key = str(p)
client.send(str_key.encode())
# etablir une cle public
server_key = g ^ alice % p
# recevoir la clé publique
client_number = int(client.recv(500))
g = int(client_number.decode("utf-8"))
# envoyer la clé publique
client.send(str(server_key).encode())
# etablir la clé partagé
cle_commune = (g ^ alice % p).to_bytes(8, "big")


def encrypt(msg):
    cipher = DES.new(cle_commune, DES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
    return nonce, ciphertext, tag


def decrypt(nonce, ciphertext, tag):
    cipher = DES.new(cle_commune, DES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        return plaintext.decode()

    except:
        print("Le message n'est pas fiable")
        raise SystemExit


while True:
    try:
        client_recv = client.recv(500)
        # décoder le message en utf-8
        if client_recv:
            nonce, cipher, tag = pickle.loads(client_recv)
        print("client: ", decrypt(nonce, cipher, tag))
        msg = input("server: ")
        msg_obj = pickle.dumps(encrypt(msg))
        client.send(msg_obj)
    except KeyboardInterrupt:
        print("fermer")
        client.shutdown(socket.SHUT_RDWR)
        socket.shutdown(socket.SHUT_RDWR)
        raise SystemExit
