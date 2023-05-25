import datetime
from errno import EBUSY
from filecmp import cmp
from re import T
import socket
import threading
import os
from threading import Thread, Lock
from datetime import date, datetime
import time
import threading
HEADER = 64
PORT = 5050
SERVER = "172.18.0.115"
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.bind(ADDR)



server=""
thread_data={}



cmp_read = Lock()#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cmp_write = Lock()#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fact_read = Lock()
fact_write = Lock()
hist_read = Lock()
hist_write = Lock()
vol_write = Lock()
vol_read = Lock()

def consulter_vol(r):  # Consulter un compte par user
    print("Etat du semaphore : " + str(cmp_read))
    cmp_read.acquire()
    with open('vol.txt', 'r') as f:
        f.readline()
        data = f.readlines()
        for x in data:
            details = x
            l = details.split("\t")
            if int(l[0]) == int(r):
                ch = l[0]+"\t"+l[1]+"\t"+l[2]+"\t"+l[3]+"\t"+l[4]
    
        cmp_read.release()
        return ch

def consulterVolAdmin(referenceVol):  # consulter un compte par admin
    cmp_read.acquire()
    ch = "0"
    with open('Vol.txt', 'r') as f:
        f.readline()
        data = f.readlines()

        for x in data:
            details = x
            l = details.split("\t")

            if int(l[0]) == int(referenceVol):
                ch = str(l[0])+"\t"+str(l[1])+"\t"+str(l[2])+"\t"+str(l[3])+"\t"+str(l[4])

        cmp_read.release()
        return ch



        
        
def afficher_agence(reference):  # consulter un compte par admin
    cmp_read.acquire()
    ch = "0"
    with open('Actuelagence.txt', 'r') as f:
        f.readline()
        data = f.readlines()

        for x in data:
            details = x
            l = details.split("\t")

            if int(l[0]) == int(reference):
                ch = str(l[0])+"\t"+str(l[1])

        cmp_read.release()
        return ch

def supprimer_vol(referenceVol):
    cmp_read.acquire()
    ch="0"
    with open('vol.txt', 'r') as f:
        f.seek(0)
        firstl=f.readline()
        lines = f.readlines()
    with open('vol.txt', 'w') as f:
        f.write(firstl)
        for line in lines:
            print(line)  
            details = line.split("\t")
            print(details)
            if (int(details[0]) != int(referenceVol)):
              
                f.write(line)  # réécrire la ligne dans le fichier
            else:
                ch="existe"
                print('fassa5na')
        
    cmp_read.release()
    return ch


def supprimer_agence(reference):
    cmp_read.acquire()
    ch="0"
    with open('Actuelagence.txt', 'r') as f:
        f.seek(0)
        firstl=f.readline()
        lines = f.readlines()
    with open('Actuelagence.txt', 'w') as f:
        f.write(firstl)
        for line in lines:
            print(line)  
            details = line.split("\t")
            print(details)
            if (int(details[0]) != int(reference)):
              
                f.write(line)  # réécrire la ligne dans le fichier
            else:
                ch="existe"
                print('fassa5na')
        
    cmp_read.release()
    return ch


def ecrire_dans_admin(ch): #ajouter dans admin
    vol_write.acquire()
    with open('profil.txt', 'a+') as f:
        f.writelines(ch+"\n")
    vol_write.release()   
    return ch

def ancienval(referenceVol):  #tester l'existance et retourner le vol s'il existe 
    ch="0"
    cmp_read.acquire()
    with open('vol.txt', 'r') as f:
        f.readline()
        data = f.readlines()

        for x in data:
            details = x
            s= details.split("\t")

            if int(s[0]) == int(referenceVol):
               ch=details
    
    cmp_read.release()
    return ch
   
def supprimer_admin(email):
    cmp_read.acquire()
    ch="0"
    with open('profil.txt', 'r') as f:
        f.seek(0)
        firstl=f.readline()
        lines = f.readlines()
    with open('profil.txt', 'w') as f:
        f.write(firstl)
        for line in lines:
            print(line)  
            details = line.split("\t")
            print(details)
            if (details[0]) != email:
              
                f.write(line)  # réécrire la ligne dans le fichier
            else:
                ch="existe"
                print('fassa5na')
        
    cmp_read.release()
    return ch

def consulterfactureAdmin(r):  # consulter
    fact_read.acquire()
    ch = "0"
    with open('facture.txt', 'r') as f:
        f.readline()
        data = f.readlines()

        for x in data:
            details = x
            l = details.split("\t")


            if int(l[0]) == int(r):
                ch = "somme à payer: "+str(l[1]).replace("\n",'')

    fact_read.release()
    return ch

def consultercmpAdmin(emailad):  # consulter un compte admin
    cmp_read.acquire()
    ch = "0"
    with open('profil.txt', 'r') as f:
        f.readline()
        data = f.readlines()

        for x in data:
            details = x
            l = details.split("\t")

            if l[0] == emailad:
                ch = str(l[0])+"\t"+str(l[1])+"\t"+str(l[2])+"\t"+str(l[3])

        cmp_read.release()
        return ch

def consulter_historiqueAdmin():
    ch = ""
    hist_read.acquire()
    with open('histo.txt', 'r') as f:
        data = f.readlines()
        for x in data:
            ch = ch + x + "\n"
        hist_read.release()
        return ch


def verifProfil(u, p):
    cmp_read.acquire()
    ch = "verifier vos donnée"
    with open("profil.txt", "r") as f:
        a = f.readline()
        data = f.readlines()
        for x in data:
            details = x
            l = details.split("\t")
            if l[0] == u and l[1] == p:
                if "user" in l[2]:
                    ch = "user"
                    print("tesst ", ch)
                    r=l[3].replace("\n",'')
                    print(r)
                else:
                    ch = "admin"
                    r=l[3].replace("\n",'')
    cmp_read.release()
    return (ch,r) 

def verifProfilUDP(u, p):
    cmp_read.acquire()
    ch = "verifier vos donnée"
    with open("profil.txt", "r") as f:
        a = f.readline()
        data = f.readlines()
        for x in data:
            details = x
            l = details.split("\t")
            if l[0] == u and l[1] == p:
                if "user" in l[2]:
                    ch = "user"
                else:
                    ch = "admin"

    cmp_read.release()
    return ch

def verifier_ref_vol(a):
    cmp_read.acquire()
    with open("vol.txt", "r") as f:
        f.readline()
        for x in f:
            details = x
            l = details.split("\t")
            if l[0] == a:
                cmp_read.release()
                return 1
        cmp_read.release()
        return 0
    

def ecrire_dans_histo(refvol, refag, transaction, valeur, resultat):
    print("neeewww!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Etat du semaphore : " + str(hist_write))
    hist_write.acquire()
    ch1 = refvol+"\t"+refag+"\t"+transaction+"\t"+valeur+"\t"+resultat+"\t"+str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))+"\n"
    with open('histo.txt', 'a+')as file1:
        file1.writelines(ch1)
    time.sleep(10)   
    print("Etat du semaphore : " + str(hist_write))
    hist_write.release()
    print("Etat du semaphore : " + str(hist_write))
    return 0


   
def ecrire_dans_vol(ch): #ajouter dans vol
    vol_write.acquire()
    with open('vol.txt', 'a+') as f:
        ch = ch+"\n"
        print("nouvelle ligne vol    ",ch)
        f.writelines(ch)
    vol_write.release()   
    return ch
    
def ajouter_agence(ch):    
    vol_write.acquire()
    with open('TTagence.txt', 'a+') as f:
        f.writelines(ch)
    vol_write.release()  
    vol_write.acquire()
    with open('Actuelagence.txt', 'a+') as f:
        f.writelines(ch)
    vol_write.release()  
    return ch

    

def consulter_historiqueAdmin():
    ch = ""
    hist_read.acquire()
    with open('histo.txt', 'r') as f:
        data = f.readlines()
        for x in data:
            ch = ch + x + "\n"
        hist_read.release()
        return ch

    

def reserver_vol(r, nbr, refag):
    cmp_read.acquire()
    ret = 0.0
    ret2 = 0.0
    with open('vol.txt', 'r') as f:
        b = f.readline()
        data = f.readlines()
    fact_read.acquire()
    with open('facture.txt', 'r') as f1:
        b1 = f1.readline()
        data1 = f1.readlines()
    i=0
    for x in data:
        i=i+1
        details = x
        l = details.split("\t")
        if int(l[0]) == int(r):
           #date_s = l[4]
           #date_str= date_s.replace("\n",'')
           #date_object = datetime.strptime(date_str, '%d-%m-%Y')
           #today = date.today()
           #if date_object.date() >= today:
           if int(nbr) <= int(l[2]):
                v = int(l[2])-int(nbr) 
                ecrire_dans_histo(l[0], refag, "demande", nbr, "succes")
                ret=float(float(nbr)*float(l[3]))
                x=l[0]+"\t"+l[1]+"\t"+str(v)+"\t"+l[3]+"\t"+l[4]
                fact_read.release()
                cmp_read.release()
                break
           else:
                ecrire_dans_histo(l[0], refag, "demande", nbr, "impossible")
                fact_read.release()
                cmp_read.release()
                return 0
           '''else:
                    ecrire_dans_histo(l[0], refag, "demande", nbr, "impossible")
                    fact_read.release()
                    cmp_read.release()
                    return -1 '''        
    data[i-1]=x
    j=0
    test=False
    for x1 in data1:
       j=j+1
       details1 = x1
       l1 = details1.split("\t")
       print("teeeeeeeeeeeessssssssssssssttttttttttttttt")
       print(l1)
       if int(l1[0]) == int(refag):
            test=True
            ret2 = l1[1]
            x1=str(refag)+"\t"+str(ret+float(ret2))+"\n"
            break  
    data1[j-1] = x1
    if test==False: 
        x2 = refag+"\t"+str(float(ret))+"\n"
        data1.append(x2)
    cmp_write.acquire()
    with open('vol.txt', 'w') as file:
        file.writelines(b)
        file.writelines(data)
    cmp_write.release()
    fact_write.acquire()
    with open('facture.txt', 'w')as file2:
        file2.writelines(b1)
        file2.writelines(data1)
    fact_write.release()
    return 1


def annuler_vol(r, nbr , refag):
    cmp_read.acquire()
    ret = 0.0
    ret2 = 0.0
    with open('vol.txt', 'r') as f:
        b = f.readline()
        data = f.readlines()
    fact_read.acquire()
    with open('facture.txt', 'r') as f1:
        b1 = f1.readline()
        data1 = f1.readlines()
    i=0
    for x in data:
        i=i+1
        details = x
        l = details.split("\t")
        if int(l[0]) == int(r):
           #date_s = l[4]
           #date_str= date_s.replace("\n",'')
           #date_object = datetime.strptime(date_str, '%d-%m-%Y')
           #today = date.today()
           #if date_object.date() >= today:
           v = int(l[2])+int(nbr) 
           ecrire_dans_histo(l[0], refag, "annulation", nbr, "succes")
           ret=float((float(nbr)*float(l[3]))+0.1*(float(nbr)*float(l[3])))
           x=l[0]+"\t"+l[1]+"\t"+str(v)+"\t"+l[3]+"\t"+l[4]
           fact_read.release()
           cmp_read.release()
           break
           '''else:
                ecrire_dans_histo(l[0], refag, "annulation", nbr, "impossible")
                fact_read.release()
                cmp_read.release()
                return -1  '''       
    data[i-1]=x
    j=0
    for x1 in data1:
       j=j+1
       details1 = x1
       m = details1.split("\t")
       if int(m[0]) == int(refag):
            test=True
            ret2 = m[1]
            x1 = str(refag)+"\t"+str(float(ret2)-ret)+"\n"
            break  
    data1[j-1]=x1
    cmp_write.acquire()
    with open('vol.txt', 'w') as file:
        file.writelines(b)
        file.writelines(data)
    cmp_write.release()
    fact_write.acquire()
    with open('facture.txt', 'w')as file2:
        file2.writelines(b1)
        file2.writelines(data1)
    fact_write.release()
    return 1

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    ref = 0
    refag = -1
    nbr = 0
    username = ""
    mdp = ""
    profil = False
    admin = False
    user = False
    while connected == True:
        while (profil == False):

            msg_length1 = conn.recv(HEADER).decode(FORMAT)
            if msg_length1:
                msg_length1 = int(msg_length1)
                msg1 = conn.recv(msg_length1).decode(FORMAT)
                username = msg1
                if msg1 == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] {msg1}")
                    break
                conn.send("__".encode(FORMAT))
            msg_length2 = conn.recv(HEADER).decode(FORMAT)
            if msg_length2:
                msg_length2 = int(msg_length2)
                msg2 = conn.recv(msg_length2).decode(FORMAT)
                mdp = msg2
                if msg2 == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] {msg2}")
                    break
            ch = verifProfil(username, mdp)[0]
            refag = verifProfil(username, mdp)[1]
            
            if (ch != 'verifier vos donnée'):
                if(ch == "user"):
                    conn.send("user".encode(FORMAT))
                    user = True
                    profil = True
                else:
                    conn.send("admin".encode(FORMAT))
                    admin = True
                    profil = True
            else:
                conn.send(ch.encode(FORMAT))
        while (user):
            msg_length1 = conn.recv(HEADER).decode(FORMAT)
            if msg_length1:
                msg_length1 = int(msg_length1)
                msg1 = int(conn.recv(msg_length1).decode(FORMAT))
                if msg1 == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg1}")
                conn.send("__".encode(FORMAT))
            msg_length2 = conn.recv(HEADER).decode(FORMAT)
            if msg_length2:
                msg_length2 = int(msg_length2)
                msg2 = conn.recv(msg_length2).decode(FORMAT)
                if msg2 == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg2}")

                if msg1 == 0:
                    ref = msg2
                    rep = verifier_ref_vol(msg2)
                    conn.send(str(rep).encode(FORMAT))
                if msg1 == 1:
                    nbr=msg2
                    rep = reserver_vol(ref, msg2, refag)
                    print(rep)
                    conn.send(str(rep).encode(FORMAT))
                    if rep == 1:
                        facture = consulterfactureAdmin(refag)
                        conn.send(str(facture).encode(FORMAT))
                if msg1 == 2:
                    nbr=msg2
                    rep = annuler_vol(ref, msg2 , refag)
                    conn.send(str(rep).encode(FORMAT))
                    facture = consulterfactureAdmin(refag)
                    conn.send(str(facture).encode(FORMAT))

                if msg1 == 3:
                    rep = consulter_vol(ref)
                    conn.send(str(rep).encode(FORMAT))
                    facture = consulterfactureAdmin(refag)
                    conn.send(str(facture).encode(FORMAT))

                if msg1 == 4:
                    profil = False
                    admin = False
                    user = False
                    rep = "utilisateur déconnecté"
                    print(rep)
                    conn.send(str(rep).encode(FORMAT))

                    break
        while (admin):
            msg_length1 = conn.recv(HEADER).decode(FORMAT)
            if msg_length1:
                msg_length1 = int(msg_length1)
                msg1 = int(conn.recv(msg_length1).decode(FORMAT))
                print(f"[{addr}] {msg1}")
                conn.send("__".encode(FORMAT))
            msg_length2 = conn.recv(HEADER).decode(FORMAT)
            if msg_length2:
                msg_length2 = int(msg_length2)
                msg2 = conn.recv(msg_length2).decode(FORMAT)
                if msg2 == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg2}")
                if msg1 == 1:
                    ref = msg2
                    rep = consulterVolAdmin(msg2)
                    conn.send(str(rep).encode(FORMAT))
                if msg1 == 2:
                    ref = msg2
                    rep = consulterfactureAdmin(msg2)
                    conn.send(str(rep).encode(FORMAT))
                if msg1 == 3:
                    ref = msg2
                    rep = consulter_historiqueAdmin()
                    conn.send(str(rep).encode(FORMAT))
                if msg1 == 5:#ajouter un vol
                    vol = msg2
                    rep = ecrire_dans_vol(vol)
                    conn.send(str(rep).encode(FORMAT))  
                if msg1 == 6: #supprimer vol 
                    vol = msg2
                    rep = supprimer_vol(msg2)
                    conn.send(str(rep).encode(FORMAT)) 
                if msg1 == 17: #supprimer vol 
                    vol = msg2
                    rep = supprimer_agence(msg2)
                    conn.send(str(rep).encode(FORMAT)) 
                if msg1 == 15: #ajouter agence 
                    ag = msg2
                    rep = ajouter_agence(msg2)
                    conn.send(str(rep).encode(FORMAT))     
                if msg1 == 21: #afficher agence 
                    ag = msg2
                    rep = afficher_agence(msg2)
                    conn.send(str(rep).encode(FORMAT))   
                if msg1 == 8:   #consulter l'ancien donnees du vol
                    vol = msg2
                    rep = ancienval(msg2)
                    conn.send(str(rep).encode(FORMAT))     
                if msg1 == 10:#ajouter un admin
                    admin = msg2
                    rep = ecrire_dans_admin(admin)
                    conn.send(str(rep).encode(FORMAT))   
                
                if msg1 == 12: #supprimer admin 
                    vol = msg2
                    rep = supprimer_admin(msg2)
                    conn.send(str(rep).encode(FORMAT))

                if msg1 == 11:
                    ref = msg2
                    rep = consultercmpAdmin(msg2)
                    conn.send(str(rep).encode(FORMAT))

                if msg1 == 4:
                    profil = False
                    admin = False
                    user = False
                    rep = "utilisateur déconnecté"
                    print(rep)
                    conn.send(str(rep).encode(FORMAT))
                    break
        continue

    conn.close()

def handle_clientUDP(ip,port):
    global server
    global ADDR
    connected = True
    ref = 0
    con = 0
    username = ""
    mdp = ""
    profil = False
    admin = False
    user = False
    while connected == True:
        while (profil == False):
            #msg_length1 = server.recvfrom(HEADER)[0].decode(FORMAT)
            msg_length1=thread_data[(ip,port)]
            print("fi wost server",msg_length1)
            if msg_length1:
                msg_length1 = int(msg_length1)
                print( (msg_length1,thread_data[(ip,port)]))
                while (str(msg_length1)==thread_data[(ip,port)]):
                    pass

                msg1 = thread_data[(ip,port)]
                username = msg1
                print("fi wost server , username=",username)
                if msg1 == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] {msg1}")
                    break
                server.sendto("ack".encode(FORMAT),(ip,port))
            while (str(msg1)==thread_data[(ip,port)]):
                pass
            msg_length2=thread_data[(ip,port)]
            if msg_length2:
                msg_length2 = int(msg_length2)
                print( (msg_length2,thread_data[(ip,port)]))
                while (str(msg_length2)==thread_data[(ip,port)]):
                    pass

                msg2= thread_data[(ip,port)]
                mdp = msg2
                print("fi wost server , mdp=",mdp)
                if msg2 == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] {msg2}")
                    break
            ch = verifProfilUDP(username, mdp)
            print("résultat vérifProfil ",ch)
            if (ch != 'verifier vos donnée'):
                if(ch == "user"):
                    server.sendto("user".encode(FORMAT),(ip,port))
                    user = True
                    profil = True
                else:
                    server.sendto("admin".encode(FORMAT),(ip,port))
                    admin = True
                    profil = True
            else:
                server.sendto(ch.encode(FORMAT),(ip,port))
        while (user):
            print("while true pass in user")
            while True:
                pass
            msg_length1 = server.recv(HEADER).decode(FORMAT)
            if msg_length1:
                msg_length1 = int(msg_length1)
                msg1 = int(server.recv(msg_length1).decode(FORMAT))
                if msg1 == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg1}")
                server.send("__".encode(FORMAT))
            msg_length2 = server.recv(HEADER).decode(FORMAT)
            if msg_length2:
                msg_length2 = int(msg_length2)
                msg2 = server.recv(msg_length2).decode(FORMAT)
                if msg2 == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg2}")

                if msg1 == 0:
                    ref = msg2
                    rep = verifier_ref_cmp(msg2)
                    server.send(str(rep).encode(FORMAT))
                if msg1 == 1:
                    rep = debiter_cmp(ref, msg2)
                    server.send(str(rep).encode(FORMAT))
                    if rep == 1:
                        facture = consulter_factureAdmin(ref)
                        server.send(str(facture).encode(FORMAT))

                if msg1 == 2:
                    rep = crediter_cmp(ref, msg2)
                    server.send(str(rep).encode(FORMAT))
                    facture = consulter_factureAdmin(ref)
                    server.send(str(facture).encode(FORMAT))

                if msg1 == 3:
                    rep = consulter_cmp(ref)
                    server.send(str(rep).encode(FORMAT))
                    facture = consulter_factureAdmin(ref)
                    server.send(str(facture).encode(FORMAT))

                if msg1 == 4:
                    profil = False
                    admin = False
                    user = False
                    rep = "utilisateur déconnecté"
                    print(rep)
                    server.send(str(rep).encode(FORMAT))

                    break

        while (admin):
            print("while true pass in admin")
            while True:
                pass
            msg_length1 = server.recv(HEADER).decode(FORMAT)
            if msg_length1:
                msg_length1 = int(msg_length1)
                msg1 = int(server.recv(msg_length1).decode(FORMAT))
                print(f"[{addr}] {msg1}")
                server.send("__".encode(FORMAT))
            msg_length2 = server.recv(HEADER).decode(FORMAT)
            if msg_length2:
                msg_length2 = int(msg_length2)
                msg2 = server.recv(msg_length2).decode(FORMAT)
                if msg2 == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg2}")
                if msg1 == 1:
                    ref = msg2
                    rep = consulter_cmpFctAdmin(msg2)
                    server.send(str(rep).encode(FORMAT))
                if msg1 == 2:
                    ref = msg2
                    rep = consulter_factureAdmin(msg2)
                    server.send(str(rep).encode(FORMAT))
                if msg1 == 3:
                    ref = msg2
                    rep = consulter_historiqueAdmin()
                    server.send(str(rep).encode(FORMAT))
                if msg1 == 4:
                    profil = False
                    admin = False
                    user = False
                    rep = "utilisateur déconnecté"
                    print(rep)
                    server.send(str(rep).encode(FORMAT))
                    break
        continue

    server.close()

def creer_fichiers():
    if os.path.isfile("vol.txt")== False:
            Vol = ["RéfVol", "Destination", "NbrPlaces", "PrixPlace","DateHeure"]
            with open("vol.txt", "w") as f:
                for c in Vol:
                    f.write(c+"\t")
                f.write("\n")

    if os.path.isfile("histo.txt")== False:                
            histo = ["RéfVol", "RéfAgence","Transaction", "Valeur", "Résultat", "DateHeure"]
            with open("histo.txt", "w") as f1:
                for h in histo:
                    f1.write(h+"\t")
                f1.write("\n")
    if os.path.isfile("facture.txt")== False:                
            facture = ["Réf", "Somme à payer"]
            with open("facture.txt", "w") as f2:
                for f in facture:
                    f2.write(f+"\t")
                f2.write("\n")
    if os.path.isfile("profil.txt")== False:                
            profil = ["Email", "Password","Role","Agence"]
            with open("profil.txt", "w") as f3:
                for f in profil:
                    f3.write(f+"\t")
                f3.write("\n")

    if os.path.isfile("TTagence.txt")== False:
            TTagence = ["RéfAgence", "Localisation"]
            with open("TTagence.txt", "w") as f4:
                for f in TTagence:
                    f4.write(f+"\t")
                f4.write("\n")
    if os.path.isfile("Actuelagence.txt")== False:               
            Actuelagence = ["RéfAgence", "Localisation"]
            with open("Actuelagence.txt", "w") as f5:
                for f in Actuelagence:
                    f5.write(f+"\t")
                f5.write("\n")


def start():
 
    global server

    bar_length = 79
    print("\n")
    print(" /$$      /$$ /$$$$$$$$ /$$        /$$$$$$   /$$$$$$  /$$      /$$ /$$$$$$$$         ")
    print("| $$  /$ | $$| $$_____/| $$       /$$__  $$ /$$__  $$| $$$    /$$$| $$_____/    ")
    print("| $$ /$$$| $$| $$      | $$      | $$  \\__/| $$  \\ $$| $$$$  /$$$$| $$              ")
    print("| $$/$$ $$ $$| $$$$$   | $$      | $$      | $$  | $$| $$ $$/$$ $$| $$$$$            ")
    print("| $$$$_  $$$$| $$__/   | $$      | $$      | $$  | $$| $$  $$$| $$| $$__/            ")
    print("| $$$/ \\  $$$| $$      | $$      | $$    $$| $$  | $$| $$\\  $ | $$| $$              ")
    print("| $$/   \\  $$| $$$$$$$$| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$ \\/  | $$| $$$$$$$$      ")
    print("|__/     \\__/|________/|________/ \\______/  \\______/ |__/     |__/|________/       ")
    print("\n")
    # Boucle pour mettre à jour la barre de chargement
    creer_fichiers()

    
    #BEGIN_____NEW

    while True:
        print("Veuillez choisir le protocle utilisé par le serveur :")
        print("1) TCP")
        print("2) UDP")
        choixModeServeur=int(input())
        if choixModeServeur==1 or choixModeServeur==2:
            break
        else:
            print("Veuillez saisir 1 ou 2")
    if(choixModeServeur==1):#=============================TCP==============================
        

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()

        print("Initiating Server", end="")
        for j in range(6):
            print(".", end="", flush=True)
            time.sleep(0.5)
        print("\n")

        for i in range(bar_length+1):
            percent = i * 100 / bar_length
            bar = '=' * i + '-' * (bar_length - i)
            print(f'[{bar}] {percent:.0f}%', end='\r')
            time.sleep(0.05)
        print("\n")

        print(f"[LISTENING] Server is listening on {SERVER}")
        print("MODE TCP !!!")
        while True:
            conn, addr = server.accept()
            thread = Thread(target=handle_client, args=(conn, addr))
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    elif(choixModeServeur==2):#=============================UDP==============================
        adresses=[]
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(('192.168.56.1', 9999))
        print("Initiating Server", end="")
        for j in range(6):
            print(".", end="", flush=True)
            time.sleep(0.5)
        print("\n")

        for i in range(bar_length+1):
            percent = i * 100 / bar_length
            bar = '=' * i + '-' * (bar_length - i)
            print(f'[{bar}] {percent:.0f}%', end='\r')
            time.sleep(0.05)
        print("\n")
        print(f"[ACTIVE] Server is Working ! on {SERVER}")
        print("MODE UDP !!!")


        while True:
            data,address=server.recvfrom(1024)
            data=data.decode(FORMAT)
            if (address not in adresses):
                adresses.append(address) 
                thread_data[address]=data
                print()

                print(f"New thread, Accepted datagram from {address}")
                datagram_thread = threading.Thread(target=handle_clientUDP, args=(address))
                datagram_thread.start()
                print("Nombre de client total en communication est :",threading.active_count())

            else:
                print(f"Old thread Accepted datagram from {address}")
                thread_data[address]=data
            #print("Nombre de client total en communication est :",threading.active_count())
  

   
  
    #server.listen()
    '''  bar_length = 79
    print("\n")
    print(" /$$      /$$ /$$$$$$$$ /$$        /$$$$$$   /$$$$$$  /$$      /$$ /$$$$$$$$         ")
    print("| $$  /$ | $$| $$_____/| $$       /$$__  $$ /$$__  $$| $$$    /$$$| $$_____/    ")
    print("| $$ /$$$| $$| $$      | $$      | $$  \\__/| $$  \\ $$| $$$$  /$$$$| $$              ")
    print("| $$/$$ $$ $$| $$$$$   | $$      | $$      | $$  | $$| $$ $$/$$ $$| $$$$$            ")
    print("| $$$$_  $$$$| $$__/   | $$      | $$      | $$  | $$| $$  $$$| $$| $$__/            ")
    print("| $$$/ \\  $$$| $$      | $$      | $$    $$| $$  | $$| $$\\  $ | $$| $$              ")
    print("| $$/   \\  $$| $$$$$$$$| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$ \\/  | $$| $$$$$$$$      ")
    print("|__/     \\__/|________/|________/ \\______/  \\______/ |__/     |__/|________/       ")
    print("\n")
    # Boucle pour mettre à jour la barre de chargement
    creer_fichiers()

    print("Initiating Server", end="")
    for j in range(6):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print("\n")

    for i in range(bar_length+1):
        percent = i * 100 / bar_length
        bar = '=' * i + '-' * (bar_length - i)
        print(f'[{bar}] {percent:.0f}%', end='\r')
        time.sleep(0.05)
    print("\n")

    print(f"[LISTENING] Server is listening on {SERVER}")
   
    while True:
        conn, addr = server.accept()
        thread = Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")'''

start()
