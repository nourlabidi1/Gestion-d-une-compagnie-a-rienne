from itertools import takewhile
import socket
from typing import no_type_check
from urllib.request import AbstractBasicAuthHandler

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.121"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg1, msg2):
    message1 = str(msg1).encode(FORMAT)
    message2 = str(msg2).encode(FORMAT)
    msg_length1 = len(message1)
    send_length1 = str(msg_length1).encode(FORMAT)
    send_length1 += b' ' * (HEADER - len(send_length1))
    client.send(send_length1)
    client.send(message1)
    rep1 = client.recv(2048).decode(FORMAT)
    msg_length2 = len(message2)
    send_length2 = str(msg_length2).encode(FORMAT)
    send_length2 += b' ' * (HEADER - len(send_length2))
    client.send(send_length2)
    client.send(message2)
    rep2 = client.recv(2048).decode(FORMAT)
    return rep2


def send_transaction():
    
    a = 0
    profil = False
    while True:
        while(profil == False):
            print("***************************************************************")
            print("******                                                   ******")
            print("******            Username :                             ******")
            username = str(input())
            print("******                                                   ******")
            print("******            Mot de passe :                         ******")
            print("******                                                   ******")
            mdp = str(input())
            print("******                                                   ******")
            print("***************************************************************")
            print("\n")
            reponse = send(username, mdp)

            if (reponse != 'Verifier vos donnée !'):
                profil = True
            while (reponse == "user" and a != 1):
                while True:
                    print("Donner la référence du vol")
                    ref = int(input())
                    rep = send(0, ref)
                    while int(rep) == 0:
                        print("référence invalide !!")
                        print("Donner la référence du vol")
                        ref = int(input())
                        rep = send(0, ref)
                    if int(rep) == 1:
                        while True:
                            print("***************************************************************")
                            print("******          MENU Agence (user)                       ******")
                            print("******                                                   ******")
                            print("******   1) Demander une réservation                     ******")
                            print("******   2) Annuler une réservation                      ******")
                            print("******   3) Demande d'une facture                        ******")
                            print("******   0) Quitter                                      ******")
                            print("******                                                   ******") 
                            print("***************************************************************")
                            t = int(input())
                            if t == 1:
                                    print("Donner le nombre de place :")
                                    nbr = int(input())
                                    rep = send(1, nbr)
                                    if int(rep) == 0:
                                        print("échec, nombre de place insuffisant !!")
                                        print("\n")
                                        continue
                                    if int(rep) == -1:
                                        print("échec, le vol est déjà passé !!")
                                        print("\n")
                                        continue
                                    if int(rep) == 1:
                                        print("opération réussie !!")
                                        fact = client.recv(2048).decode(FORMAT)
                                        print("votre facture est\t"+fact)
                                        print("\n")
                                        continue
                            if t == 2:
                                    print("Donner le nombre de place à annuler :")
                                    nbr = int(input())
                                    rep = send(2, nbr)
                                    if int(rep) == -1:
                                        print("échec, le vol est déjà passé !!")
                                        print("\n")
                                        continue
                                    else:
                                        print("opération réussie !!")
                                        fact = client.recv(2048).decode(FORMAT)
                                        print("votre facture est :"+fact)
                                        print("\n")
                                    continue
                            if t == 3:
                                    rep = send(3, 0)
                                    print("les informations du vol est \n :" + rep)
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
                print("***************************************************************")
                print("******          MENU Compagnie (Admin)                   ******")
                print("******                                                   ******")
                print("******   1) Gestion des vols                             ******")
                print("******   2) Gestion des admins                           ******")
                print("******   3) Gestion des agences                          ******")
                print("******   4) Consulter la facture d’une agence            ******")
                print("******   5) Consulter l’historique des transactions      ******")
                print("******   0) Quitter                                      ******")
                print("******                                                   ******") 
                print("***************************************************************")
                t = int(input())
                if t == 1:
                   while True:
                    print("***************************************************************")
                    print("******          Gestion des vols                         ******")
                    print("******                                                   ******")
                    print("******   1) Ajouter un vol                               ******")
                    print("******   2) Modifier un vol                              ******")
                    print("******   3) Supprimer un vol                             ******")
                    print("******   4) Consulter un vol                             ******")
                    print("******   0) Quitter                                      ******")
                    print("******                                                   ******") 
                    print("***************************************************************") 
                    v= int(input())
                    if v ==1:
                        vol=""
                        print("Donner les donnees du vol :")
                        print("la reference :")
                        ref=int(input())
                        print("la Destination :")
                        dest=str(input())
                        print("le nombre des places :")
                        nbrp=int(input())
                        print("le prix d'une  place :")
                        prixp=float(input())
                        print("la date :")
                        date=str(input())
                    
                        vol+=str(ref)+"\t"+str(dest)+"\t"+str(nbrp)+"\t"+str(prixp)+"\t"+str(date)
                        rep = send(5,vol)
                        if rep == "0":
                                    print("Vol existe déja  !!")
                                    print("\n")
                                    continue
                        else:
                                    print("le vol a été ajouté :\n")
                                    print("Reference"+"\t"+"Destination"+"\t"+"NombrePlaces"+"\t"+"PrixPlace"+"\t"+"DateHeure"+"\n")
                                    print(rep)
                                    continue  
                    if v ==2:
                        ch=""
                        print("Donner la reference du vol:")
                        ref=int(input())
                        l = send(1, ref)
                        if l == "0":
                            print("Ce vol n existe pas   !!")
                            print("\n")
                            continue
                        else:
                            k=l.split("\t")
                            ch+=str(ref)+"\t"
                            print("Donner les nouvelles données du vol :")
                            print("la Destination , si vous ne voulez pas changer cette valeur tapez N sinon entrer la nouvelle destination  ")
                            dest=str(input())
                            if (dest== 'N'):
                                ch+=k[1]+"\t"
                            else :
                                ch+= str(dest)+"\t"
                
                            print("le nombre des places ,si vous ne voulez pas changer cette valeur tapez 0 sinon entrer la nouvelle valeur:")
                            nbp=int(input())
                            if (nbp== 0):
                                ch+= str(k[2])+"\t"
                            else :
                                ch+= str(nbp)+"\t"
                            print("le prix d'une  place ,si vous ne voulez pas changer cette valeur tapez 0 sinon entrer la nouvelle valeur:")
                            prixv=float(input())
                            if (prixv== 0):
                                ch+= str(k[3])+"\t"
                            else :
                                ch+= str(prixv)+"\t"

                            
                            rep = send(6, ref)
                            rep = send(5,ch)
                            rep = send(1,ref)
                            print("les données du  vol mises à jour sont :\n")
                            print("Reference"+"\t"+"Destination"+"\t"+"NombrePlaces"+"\t"+"PrixPlace"+"\t"+"DateHeure"+"\n")
                            print(rep)
                            continue
                                        
                    if v ==3:
                        print("Donner référence du vol :")
                        referenceVol = int(input())
                        rep = send(6,referenceVol)
                        if rep == "0":
                                    print("réference invalide !!")
                                    print("\n")
                                    continue
                        else:
                                    print("le vol a été supprimé !!\n")
                                    continue      
                    if v == 4:
                                print("Donner référence du vol :")
                                referenceVol = int(input())
                                rep = send(1, referenceVol)
                                if rep == "0":
                                    print("réference invalide !!")
                                    print("\n")
                                    continue
                                else:
                                    print("les données de ce vol sont :\n")
                                    print("ref"+"\t"+"Destination"+"\t"+"NombrePlaces"+"\t"+"PrixPlace"+"\t"+"DATEHEURE"+"\n")
                                    print(rep)
                                continue     
                    if v == 0:
                      break
                if t == 2:
                    while True:
                        print("*************************************************************")
                        print("****          Gestion des Profils                        ****")
                        print("****                                                     ****")
                        print("****   1) Ajouter un profil                              ****")
                        print("****   2) Modifier un profil                             ****")
                        print("****   3) Supprimer un profil                            ****")
                        print("****   4) Consulter un profil                            ****")
                        print("****   0) Quitter                                        ****")
                        print("****                                                     ****") 
                        print("*************************************************************")

                        a= int(input())
                        if a ==1:
                            admin=""
                            print("Donner les donnees du compte :")
                            print("l'email :")
                            email=str(input())
                            print("le mot de passe :")
                            mdp=str(input())
                            print("le type du compte:")
                            typee=str(input())
                            print("la reference de l agence:")
                            ref=int(input())

                            admin+=str(email)+"\t"+str(mdp)+"\t"+str(typee)+"\t"+str(ref)+"\n"
                            rep = send(10,admin)
                            if rep == "0":
                                        print("le profil existe déja  !!")
                                        print("\n")
                                        continue
                            else:
                                        print("le profil a été ajouté :\n")
                                        continue  
                        if a ==2:
                            ch=""
                            print("Donner l'email du profil: ")
                            email=input()
                            l = send(11, email)
                            if l == "0":
                                print("le profil n'existe pas   !!")
                                print("\n")
                                continue
                            else:
                                k=l.split("\t")
                                ch+=str(email)+"\t"
                                print("Donner les nouvelles données du profil :")
                                print("le mot de passe ,si vous ne voulez pas changer cette valeur tapez N sinon entrer la nouvelle valeur:")
                                mdp=input()
                                if (mdp== 'N'):
                                    ch+= str(k[1])+"\t"
                                else :
                                    ch+= str(mdp)+"\t"
                                print("le role ,si vous ne voulez pas changer cette valeur tapez N sinon entrer la nouvelle valeur:")
                                role=input()
                                if (role== 'N'):
                                    ch+= str(k[3])+"\t"
                                else :
                                    ch+= str(role)+"\t"
                                
                                print("le numéro d'agence ,si vous ne voulez pas changer cette valeur tapez 0 sinon entrer la nouvelle valeur:")
                                numag=int(input())
                                if (numag== 0):
                                    ch+= str(k[3])+"\t"
                                else :
                                    ch+= str(numag)+"\t"
                                rep = send(12, email)
                                rep = send(10,ch)
                                rep = send(11,email)
                                print("les données du  du profil mises à jour sont :\n")
                                print("email"+"\t"+"mot de passe"+"\t"+"role"+"\t"+"numéro agence"+"\n")
                                print(rep)
                                continue
                                            
                        if a ==3:
                            print("Donner email du profil :")
                            email = input()
                            rep = send(12,email)
                            if rep == "0":
                                        print("email invalide !!")
                                        print("\n")
                                        continue
                            else:
                                        print("le profil a été supprimé !!\n")
                                        continue      
                        if a == 4:
                                    print("Donner email du profil :")
                                    adr = str(input())
                                    rep = send(11, adr)
                                    if rep == "0":
                                        print("réference invalide !!")
                                        print("\n")
                                        continue
                                    else:
                                        print("les données du  de du profil sont :\n")
                                        print("email"+"\t"+"mot de passe"+"\t"+"role"+"\t"+"numéro agence"+"\n")
                                        print(rep)
                                    continue     
                        if v == 0:
                             break
                if t==3:
                    while True :
                        print("***************************************************************")
                        print("******          Gestion des agences                      ******")
                        print("******                                                   ******")
                        print("******   1) Ajouter une agence                           ******")
                        print("******   2) Modifier une agence                          ******")
                        print("******   3) Supprimer une agence                         ******")
                        print("******   4) Consulter une agence                         ******")
                        print("******   0) Quitter                                      ******")
                        print("******                                                   ******") 
                        print("***************************************************************")
                        c= int(input())
                        if c ==1:
                            ag=""
                            print("Donner les donnees de lagence :")
                            print("la reference :")
                            ref=int(input())
                            print("la localisation :")
                            loc=str(input())
                            ag+=str(ref)+"\t"+str(loc)+"\n"
                            rep = send(15,ag)
                            if rep == "0":
                                        print("l agence existe deja  !!")
                                        print("\n")
                                        continue
                            else:
                                        print("l agence a été ajoutée :\n")
                                        print("Reference"+"\t"+"Localisation"+"\n")
                                        print(rep)
                                        continue 
                        if c ==2:
                            ch=""
                            print("Donner la reference de l agence:")
                            ref=int(input())
                            l = send(12, ref)
                            if l == "0":
                                print("Cette agence n existe pas    !!")
                                print("\n")
                                continue
                            else:
                                k=l.split("\t")
                                ch+=str(ref)+"\t"
                                print("Donner la nouvelle localisation de l agnece :")
                                loc=str(input())
                                ch+=str(loc)
                                rep = send(17, ref)
                                rep = send(15,ch)
                                rep = send(12,ref)
                                print("les données de l agence mises à jour sont :\n")
                                print("Reference"+"\t"+"localisation"+"\n")
                                print(rep)
                                continue
                        if c==3:
                            print("Donner référence de lagence :")
                            ref = int(input())
                            rep = send(17,ref)
                            if rep == "0":
                                    print("réference invalide !!")
                                    print("\n")
                                    continue
                            else:
                                    print("la reference a été supprimée !!\n")
                                    continue    
                        if c ==4:
                                print("Donner la reference de l agence :")
                                reference = int(input())
                                rep = send(21, reference)
                                if rep == "0":
                                    print("réference invalide !!")
                                    print("\n")
                                    continue
                                else:
                                    print("les données de l agence :\n")
                                    print("ref"+"\t"+"localisation")
                                    print(rep)
                                continue   
                        if c ==0:
                            break
                if t ==4:
                    print("Donner référence de l'agence :")
                    referenceAgence = int(input())
                    rep = send(2, referenceAgence)
                    if rep == "0":
                        print("réference invalide !!")
                        print("\n")
                        continue
                    else:
                        print("la facture de cette agence est :" + rep)
                        print("\n")
                        continue

                if t==5:
                    rep = send(3, 0)
                    print("l'historique' :\n" + rep)
                    print("\n")
                if t == 0:
                    a = 1
                    reponse = send(4, 0)
                    break

             

        if a == 1:
            print("***************************************************************")
            print("******                                                   ******") 
            print("******       voulez vous se connecter de nouveau?        ******")
            print("******       1) Oui                                      ******")
            print("******       2) Non                                      ******")
            print("******                                                   ******")
            print("***************************************************************")
            c = int(input())
            if c == 1:
                a = 0
                profil = False
                continue
            elif c == 2:
                print("***************************************************************")
                print("******                                                   ******") 
                print("******                 Au Revoir!                        ******")
                print("******                                                   ******")
                print("***************************************************************")
                break
            else:
                print("***************************************************************")
                print("******                                                   ******")
                print("******    Veuillez insérer un bon choix du menu !        ******")
                print("******                                                   ******")
                print("***************************************************************")
    send("9", DISCONNECT_MESSAGE)


send_transaction()
