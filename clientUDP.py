from itertools import takewhile
import socket
from typing import no_type_check
from urllib.request import AbstractBasicAuthHandler

HEADER = 64
PORT = 9999
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def send(msg1, msg2):
    global client
    message1 = str(msg1).encode(FORMAT)
    message2 = str(msg2).encode(FORMAT)
    msg_length1 = len(message1)
    send_length1 = str(msg_length1).encode(FORMAT)
    #send_length1 += b' ' * (HEADER - len(send_length1))
    client.sendto(send_length1,ADDR)

    #print("houni1", send_length1)
    client.sendto(message1,ADDR)
    print(message1)
    #print("houni1.1")
    rep1 = client.recvfrom(2048)[0].decode(FORMAT)
    #print("houni1.2")
    msg_length2 = len(message2)
    send_length2 = str(msg_length2).encode(FORMAT)
    #send_length2 += b' ' * (HEADER - len(send_length2))
    #print("houni2")
    client.sendto(send_length2,ADDR)
    client.sendto(message2,ADDR)
    rep2 = client.recvfrom(2048)[0].decode(FORMAT)
    #print("houni3")
    return rep2


def send_transaction():
    a = 0
    profil = False
    while True:
        while(profil == False):

            print("username :")
            username = str(input())
            print("mot de passe :")
            mdp = str(input())
            reponse = send(username, mdp)

            if (reponse != 'verifier vos donnée'):
                profil = True
        while (reponse == "user" and a != 1):
            while True:
                print("Donner la référence du compte")
                ref = int(input())
                rep = send(0, ref)
                while int(rep) == 0:
                    print("référence invalide !!")
                    print("Donner la référence du compte")
                    ref = int(input())
                    rep = send(0, ref)
                if int(rep) == 1:
                    while True:

                        print("choisir Transaction")
                        print("1) Débiter")
                        print("2) Créditer")
                        print("3) Consulter Solde")
                        print("0) Quitter")
                        t = int(input())
                        if t == 1:
                            print("Donner montant :")
                            mnt = int(input())
                            rep = send(1, mnt)
                            if int(rep) == 0:
                                print("échec, montant invalide !!")
                                print("\n")
                                continue
                            if int(rep) == 1:
                                print("opération réussie !!")
                                fact = client.recv(2048).decode(FORMAT)
                                print("votre facture est\t"+fact)
                                print("\n")
                                continue
                        if t == 2:
                            print("Donner montant :")
                            mnt = int(input())
                            rep = send(2, mnt)
                            print("opération réussie !!")
                            fact = client.recv(2048).decode(FORMAT)
                            print("votre facture est\t"+fact)
                            print("\n")
                            continue
                        if t == 3:
                            rep = send(3, 0)
                            print("votre solde est \t :" + rep)
                            fact = client.recv(2048).decode(FORMAT)
                            print("votre facture est\t"+fact)
                            print("\n")
                        if t == 0:
                            a = 1
                            reponse = send(4, 0)

                            break
                break
            break

        while (reponse == "admin" and a != 1):
            while True:
                print("choisir Operation")
                print("1) Consulter un compte")
                print("2) Consulter la facture d\'un compte")
                print("3) Consulter historique")
                print("0) Quitter")
                t = int(input())
                if t == 1:
                    print("Donner référence du compte :")
                    ref = int(input())
                    rep = send(1, ref)
                    if rep == "0":
                        print("réference invalide !!")
                        print("\n")
                        continue
                    else:
                        print("les données de ce compte sont :" + rep)
                        print("\n")
                        continue
                if t == 2:
                    print("Donner référence du compte :")
                    ref = int(input())
                    rep = send(2, ref)
                    if rep == "0":
                        print("réference invalide !!")
                        print("\n")
                        continue
                    else:
                        print("la facture de ce compte est :" + rep)
                        print("\n")
                        continue
                if t == 3:
                    rep = send(3, 0)
                    print("l'historique' :\n" + rep)
                    print("\n")
                if t == 0:
                    a = 1
                    reponse = send(4, 0)
                    break

        if a == 1:
            print("voulez vous se connecter de nouveau? \n")
            print("     1)Oui\n")
            print("     2)Non\n")
            c = int(input())
            if c == 1:
                a = 0
                profil = False
                continue
            else:
                print("Au Revoir!")
                break
    send("9", DISCONNECT_MESSAGE)


send_transaction()
