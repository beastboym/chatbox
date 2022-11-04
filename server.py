import socket, pickle
from Crypto.Cipher import DES
from secrets import token_bytes

Key = token_bytes(8)

host = "127.0.0.1"
port = 6007
p = 433333333  # Nombre premier arbitraire (public)
server_number = 145111113  # nombre arbitraire inférieur à p-1


# déclarer un socket
server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# identifier le socket en server
server.bind((host, port))
server.listen(1)

# attend une connexion
client, ip = server.accept()

# Algorithme deffie hellman
# recevoir le premier nombre pour l'etablissement de clé
key = client.recv(500)
g = int(key.decode("utf-8"))
# envoyer notre chiffre de depart
str_key = str(p)
client.send(str_key.encode())
# etablir une cle public
server_key = g ^ server_number % p
# recevoir la clé publique
client_number = client.recv(500)
g = int(client_number.decode("utf-8"))
# envoyer la clé publique
client.send(str(server_key).encode())
# etablir la clé partagé
cle_commune = g ^ server_number % p


def encrypt(msg):
    cipher = DES.new(bytes(8), DES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode("ascii"))
    return nonce, ciphertext, tag


def decrypt(nonce, ciphertext, tag):
    cipher = DES.new(bytes(8), DES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        return plaintext.decode()

    except:
        print("probleme")
        return 1


while True:
    client_recv = client.recv(500)
    # décoder le message en utf-8
    nonce, cipher, tag = pickle.loads(client_recv)
    print("client: ", decrypt(nonce, cipher, tag))
    # si le message est vide on ferme
    if not client_recv:
        print("fermer")
        break
    msg = input("server: ")
    msg_obj = pickle.dumps(encrypt(msg))
    client.send(msg_obj)

client.close()
socket.close()
