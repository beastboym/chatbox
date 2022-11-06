# RAPPORT d'explication

**Daouda Kanoute 19000407**

---

Pour mon projet j'ai choisi de faire une chatbox utilisant le chiffrement DES et le protocole d'echange de clé Deffie hellman, dans ce rapport je compte donner une explication de ces deux protocoles, je ferait l'impasse sur le fonctionnement de la communication réseaux car ce n'est pas ce qui nous interresse ici.

---

## lgorithme d’échange de clés Diffie-Hellman

[ressource](https://www.bibmath.net/crypto/index.php?action=affiche&quoi=moderne/difhel)

- **A quoi cela sert-il ?**

  Abdel et Fabien souhaitent discuter de maniere sécurisé, donc souhaitent utilisé un algorithme de chiffrement (ici DES), l'utilisations de l'algorithme requiert cependant une clé, malheureusement ils ne disposent pas de support suffisament sûre pour se la transmettre, comment font-ils ? c'est à cela que sert un algorithme d'echange de clé.

- **Pourquoi cet algorithme en particulier ?**
  Il s'agit d'un des algorithmes les plus connues du genre, et à marquer l'histoire de la cryptographie. Il reste très difficile à casser meme de nos jours.

- **Est-il fiable ?**
  Oui, mais présente tout de meme un probleme, les utilisateurs doivent etre connecté au meme moment si l'un.e est absent l'echange ne pourra pas avoir lieu.
  **Fonctionnement**
  Etape 1 : Alice et Bob choisissent 2 nombres p (premier) et g (génerateur), p sera un grand nombre premier et g sera un grand nombre premer inferier à p. Ils s'echangeront ces nombres en clairs car cela n'a pas besoin d'etre sécurisé.

  Etape 2 : Alice et Bob choisissent de leurs coté (secrètement) un nombre arbitraire inferieur à p-1, X et X1.

  Etape 3 : Alice calcule Y : `g ^ X mod p` , Bob calcule Y1: `g ^ X1 mod p`

  Etape 4 : Alice et Bob s'échange Y et Y1, en clair car cela n'a pas besoin détre sécurisé.

  Etape 5 : Alice calcule Z : `Y1 ^ X mod p`, Bob calcule `Y ^ X1 mod p`

A la fin du processus alice et Bob ont la meme clé.

---

## Chiffrement DES

[ressource 1](https://web.maths.unsw.edu.au/~lafaye/CCM/crypto/des.htm)
[ressource 2](https://pycryptodome.readthedocs.io/en/latest/src/cipher/des.html)

- **Qu'est ce que c'est ?**
  Il s'agit d'un algorithme de chiffrement sysmetrique plus précisément chiffrement par bloc, utilisant des clé de 56 bits (8 octet).

- **Pourquoi cet algorithme en particulier ?**
  Il s'agit d'un des algorithmes les plus connues du genre, et à marquer l'histoire de la cryptographie, malgré le fait qu'il soit ""obsolete" aujord'hui.

- **Est-il fiable ?**
  Non, il ne l'est pas. Son espace de clés trop petit pour notre époque le rendant "facilement" cassable grace a une attaque par force brute et il est lent. Il est préferable de s'orienter vers un algorithme comme AES ou autres.

**Fonctionnement**

Les grandes lignes de l'algorithme sont les suivantes :

- Fractionnement du texte en blocs de 64 bits (8 octets)
- Permutation initiale des blocs
- Découpage des blocs en deux parties: gauche et droite, nommées
- Etapes de permutation et de substitution répétées 16 fois (appelées rondes)
- Recollement des parties gauche et droite puis permutation initiale inverse.

Pour l'implementation j'ai décidé d'utiliser pycryptodome.

Fonction de chiffrement : `def encrypt(msg):`
`cipher = DES.new(cle_commune, DES.MODE_EAX)`
Je commence par definir la variable cipher en tant que chiffrement DES qui prendra en argument la cle commune (clé privée), qui à été générer par Alice et Bob plus tôt, je déclare aussi que je souhaite quìl utilise le mode [EAX](https://en.wikipedia.org/wiki/EAX_mode), ce qui me retourna un object qui possede un nonce, un nombre aleatoire inchangeable et qui ne sera utilisé qu'une seule fois, que je garde dans une variables `nonce = cipher.nonce`.
`ciphertext, tag = cipher.encrypt_and_digest(msg.encode())`, j'utilise ensuite le cipher pour chiffrer mon message ce qui me retournera ciphertext (en bytes) puis je l'encode dans le format approprier étant donner que je n'ai rien préciser le format par défaut sera le `utf-8` , la raison pour laquelle j'ai utilisé `encrypt_and_digest`est qu'il me retourne aussi un tag qui sera utilisé pour la signature du messages, cet methode est aussi une des raison qui m'ont pousser à utilisé le mode [EAX](https://en.wikipedia.org/wiki/EAX_mode), car `encrypt_and_digest`n'est supporté que par les [mode](https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html) modernes pour le chiffrement par bloc.
La fonction `encrypt()`retourne le nonce, le ciphertext et le tag.

Fonction de déchiffrement : `def decrypt(nonce, ciphertext, tag):`
`cipher = DES.new(cle_commune, DES.MODE_EAX, nonce=nonce)`
Je commence par déclarer la variable cipher en tant que chiffrement DES qui prendra en argument la cle commune (clé privée), pour les meme raison que précedemment, la difference est que j'y ajoute mon nonce, pour éviter qu'il ne génere un nouveaux nonce et n'empeche le dechiffrement du message qui sera alors "altéré" par ce nouveaux nonce.

    plaintext = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        return plaintext.decode()

    except:
        print("probleme")
        return 1

Je déchiffre le ciphertext à l'aide de la méthode `decrypt` et verifie ensuite si le tag est correct si il est correcte je le decode (par defaut `utf-8`) et je renvoie le message en clair. Le mode [EAX](https://en.wikipedia.org/wiki/EAX_mode) me permet d'utiliser la fonction `decrypt_and_verify`que je n'ai pas utilisé. Si le tag est incorrecte cela signifie qu'il y'a eu un probleme entre l'envoi et la reception, alors je quitte le programme.
