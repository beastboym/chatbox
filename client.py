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
print("clé: ", p)
# etablir une cle public
server_number = g ^ client_number % p
print(server_number)
# envoyer la clé publique
client.send(str(server_number).encode())
# recevoir la clé publique
server_key = client.recv(500)
g = int(server_key.decode("utf-8"))
cle_commune = g ^ client_number % p
print("code: ", cle_commune)


def encrypt(msg):
    cipher = DES.new(bytes(8), DES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode("ascii"))
    print("tag: ", tag)
    print("ciphertext: ", ciphertext)

    return ciphertext, tag


def decrypt(ciphertext, tag):
    cipher = DES.new(bytes(8), DES.MODE_EAX)
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
    server_recv = server_recv.decode("utf-8")
    print("server: ", server_recv)
