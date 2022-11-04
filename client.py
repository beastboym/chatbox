import socket, pickle
from Crypto.Cipher import DES
from secrets import token_bytes

Key = token_bytes(8)
g = 233333313  # entier inférieur à p (public)
client_number = 333333333  # nombre arbitraire inférieur à p-1


host = "127.0.0.1"
port = 6007

# déclarer un socket
client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect((host, port))

# Algorithme deffie hellman
str_key = str(g)
client.send(str_key.encode())
# recevoir le premier nombre pour l'etablissement de clé
key = client.recv(500)
p = int(key.decode("utf-8"))
# etablir une cle public
server_number = g ^ client_number % p
# envoyer la clé publique
client.send(str(server_number).encode())
# recevoir la clé publique
server_key = client.recv(500)
g = int(server_key.decode("utf-8"))
cle_commune = (g ^ client_number % p).to_bytes(8, "big")


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
        print("probleme")
        return 1


nom = input("quel est votre nom :")
while True:
    msg = input(f"{nom} : ")
    msg_obj = pickle.dumps(encrypt(msg))
    client.send(msg_obj)

    server_recv = client.recv(500)
    nonce, cipher, tag = pickle.loads(server_recv)
    server_recv = decrypt(nonce, cipher, tag)
    print("server: ", server_recv)
