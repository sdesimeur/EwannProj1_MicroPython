###########################################################################
# Setup code goes below, this is called once at the start of the program: #
###########################################################################
import time
import mywifi
import network
import gc
from machine import ADC
from machine import Timer
try:
  import usocket as socket
except:
  import socket

#tim = Timer(-1)

class MagnetObj:
    def __init__(self):
        self.adc = ADC(0)
        self.tim = Timer(-1)
        self.isInInit = False
        self.Mean = 0.0
        self.Value = 0.0
        self.MinValue = 1000000000000000000.0
        self.MaxValue = -1000000000000000000.0
        self.tim.init(period=20, mode=Timer.PERIODIC, callback=self.readValue)

    def readValue(self,t):
        self.Value = self.adc.read()
        self.Value *= 3.3*3;
        self.Value /= 2048;
        self.Value /= 18;
        if (self.isInInit):
            if (self.MinValue > self.Value):
                self.MinValue = self.Value
            if (self.MaxValue < self.Value):
                self.MaxValue = self.Value
            self.Mean = (self.MinValue + self.MaxValue) / 2
            #print("Min:"+str(self.MinValue))
            #print("Max:"+str(self.MaxValue))
            #print("Mean:"+str(self.Mean))

magnet = MagnetObj()


def magnetReadValue(t):
    global magnet
    magnet.readValue()

def web_page():
    f = open("index.html")
    html = str(f.read())
    f.close()
    return html

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(mywifi.essid, mywifi.password)
    while not wlan.isconnected():
        pass
wlan.ifconfig(('192.168.4.249', '255.255.255.0', '192.168.4.1', '192.168.4.1'))

#wlan = network.WLAN(network.STA_IF)
#wlan.ifconfig(('192.168.4.249', '255.255.255.0', '192.168.4.1', '192.168.4.1'))
#wlan.active(True)
#time.sleep(5.0)
#if (wlan.isconnected() != True):
#    print("Wlan not  connected")
#    wlan.connect(mywifi.essid, mywifi.password)
#    time.sleep(3.0)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='Ewann')
ap.ifconfig(('192.168.254.1', '255.255.255.0', '192.168.254.1', '192.168.254.1'))


socketServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServeur.bind(('', 80))
socketServeur.listen(5)

def main():
    global magnet
    reponse = ""
    #tim.init(period=20, mode=Timer.PERIODIC, callback=magnetReadValue)
    #tim.init(period=20, mode=Timer.PERIODIC, callback=lambda t:print(2))
    while True:
        try:
            if gc.mem_free() < 102000:
                gc.collect()
    
            #print(wlan.ifconfig())
            #print(ap.ifconfig())
            #print("Attente connexion d'un client")
            connexionClient, adresse = socketServeur.accept()
            connexionClient.settimeout(4.0)
            #print("Connecté avec le client", adresse)
    
            #print("Attente requete du client")
            requete = connexionClient.recv(1024)     #requête du client
            requete = str(requete)
            #print("Requete du client = ", requete)
            connexionClient.settimeout(None)
    
            #print("Envoi reponse du serveur : code HTML a afficher")
            connexionClient.send('HTTP/1.1 200 OK\n')
            #connexionClient.send("Connection: close\n\n")
            #analyse de la requête, recherche de led=on ou led=off
            reponse = ""
            if "POST /configMagneto/0" in requete:
                connexionClient.send('Content-Type: text/plain\n\n\n')
                magnet.isInInit = False
            elif "POST /configMagneto/1" in requete:
                connexionClient.send('Content-Type: text/plain\n\n\n')
                magnet.MinValue = 1000000000000000000.0
                magnet.MaxValue = -1000000000000000000.0
                magnet.Mean = 0.0
                magnet.isInInit = True
            elif "POST /getMagnetField" in requete:
                connexionClient.send('Content-Type: text/plain\n\n')
                val = magnet.Value-magnet.Mean
                reponse = str(val)
                #print(reponse)
            else: 
                connexionClient.send('Content-Type: text/html\n\n')
                reponse = web_page()
            #print(reponse)
            connexionClient.sendall(reponse)
            connexionClient.close()
            #print("Connexion avec le client fermee")
    
        except:
            try:
                connexionClient.close()
                print("Connexion avec le client fermee, le programme a declenché une erreur")
            except:
                reponse = ""
                print("Pb with connexionClient")


