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
print("connexion etablie avec : ", ip)

# Algorithme deffie hellman
# recevoir le premier nombre pour l'etablissement de clé
key = client.recv(500)
g = int(key.decode("utf-8"))
print("clé: ", g)
# envoyer notre chiffre de depart
str_key = str(p)
client.send(str_key.encode())
# etablir une cle public
server_key = g ^ server_number % p
print(server_key)
# recevoir la clé publique
client_number = client.recv(500)
g = int(client_number.decode("utf-8"))
# envoyer la clé publique
client.send(str(server_key).encode())
# etablir la clé partagé
cle_commune = g ^ server_number % p
print("code secret", cle_commune)


def encrypt(msg):
    cipher = DES.new(bytes(8), DES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode("ascii"))
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


while True:
    client_recv = client.recv(150)
    # décoder le message en utf-8
    d = pickle.loads(client_recv)
    cipher, tag = d
    print("client: ", d)
    print("cipher: ", cipher)
    print("decode: ", decrypt(cipher, tag))
    # si le message est vide on ferme
    if not client_recv:
        print("fermer")
        break
    msg = input("server: ")
    msg = msg.encode("utf-8")
    client.send(msg)

client.close()
socket.close()
