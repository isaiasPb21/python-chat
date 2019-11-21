import socket
from threading import *
import time


minha_chaveE = 3568
minha_chaveN = 5647
nome = 'Abel'
cont=0
 
        # ************************************************
def enviarChaves(delay):
    global cont
    cont+=1
    try:
    
       print('Entrou no enviarCh')  
       ip = '192.168.15.2'
       port = 2121
       add = (ip, port)   
       clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       time.sleep(3)
       print(delay)
       clientSocket.connect(add)
   
       y = '#1-' + str(minha_chaveE) + "=" + str(minha_chaveN) + '+' + nome + '*'
       
       clientSocket.sendto(y.encode(), (ip, port))   
       print('Chaves que foi enviada' + y)       
       clientSocket.close()
       
    except ConnectionRefusedError:
       print('ConnectionRefusedError : Não foi possivel enviar as chaves')
       enviarChaves(5)
       
       

        # ************************************************
enviarChaves(5)
print(cont, ' tentativas .')

'''f = Thread(target=enviarChaves(5))
f.start()'''

        
        # ************************************************  
        # ************************************************       
        # ************************************************            
        # ************************************************
        # ************************************************






