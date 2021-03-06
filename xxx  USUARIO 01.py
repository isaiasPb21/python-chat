from threading import *   
from datetime import *
from tkinter import *
from tkinter import messagebox  
import socket
import time
import random

contx = 0

class Aplicacao ():
    def __init__(self, master=None):        
        self.fontePadrao = ("Verdana", "13")

        alfabeto = ['ª','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','â','ã','á','à','é','ç','õ','0','1','2','3','4','5','6','7','8','9',' ',',','.','+','-','*',':','/','\\','!','@','#','$','%','&','(',')']
        
        # ********************************************************************************************************************** FUNÇÕES
        ''' Horário do sistema '''
        def horario():
            horario = datetime.now()
            horario = horario.strftime('%H:%M %Y %S')
            return horario
        # ************************************************
        # ************************************************
        ''' Calculo das chaves '''
        def calcAlea (fim=1000):                 
            aleatorio = random.randint(0,fim)
            return aleatorio 

        def calcPrimo (num):                      
            acumulador = 0
            for n in range(1,num+1,1):
                aux = (num % n)
                if aux == 0:
                    acumulador += 1
                if (aux ==0) and (n != 1) and (n !=num):
                    return calcPrimo(num+1)
            if acumulador <= 2:
                return num
        
        numP = calcPrimo(calcAlea())     
        numQ = calcPrimo(calcAlea())

        feedN = ((numP-1) * (numQ-1))                   

        minha_chaveE = calcPrimo(calcAlea(feedN-200))
        minha_chaveN = (numP * numQ)

        chaves = (minha_chaveE, minha_chaveN)

        minha_chaveD = 0
        x=0
        while x < minha_chaveN:
            r = (x * minha_chaveE) % feedN
            if r == 1:
                minha_chaveD = x
                break
            x += 1

        print('P {} * Q {} * N {} * D {} * E {}'.format(numP, numQ, minha_chaveN, minha_chaveD, minha_chaveE))
        # ************************************************
        # ************************************************
        ''' Envia as chaves de forma 'automática'  '''
        def enviarChaves():            
            global contx
            contx += 1
            time.sleep(3)
            try:
               nome = self.ed2.get()
               print('Entrou no enviarCh')  
               ip = '192.168.15.2'
               port = 2121
               add = (ip, port)   
               clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

               clientSocket.connect(add)   
               y = '#1-' + str(minha_chaveE) + "=" + str(minha_chaveN) + '+' + nome + '*'
               
               clientSocket.sendto(y.encode(), (ip, port))   
               print('Chaves que foi enviada' + y)
               clientSocket.close()
            except :
               print('ConnectionRefusedError : Não foi possivel enviar as chaves')
               enviarChaves()

        # ************************************************
        # ************************************************
        ''' Recebe as mensagens, usando Thread '''
        def recebeMensagem ():
            print('Recebimento aberto')
            host = '192.168.15.8'
            port = 2121
            add = (host, port)   
            serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serv_socket.bind(add)
            serv_socket.listen(10)

            while True:
                 global outro_chaveE, outro_chaveN
                 con, cliente = serv_socket.accept()
                 recebe = con.recv(2024)
                 recebe = recebe.decode()  
                 print('Mensagem Recebida : ', recebe)   #

                 ''' Separando as chaves recebidas e o nome. Através de marcadores : '#' '1' '-'  '''
                 if (recebe[0] == '#') and (recebe[1] == '1') and (recebe[2] == '-'):
                     print('Ow shit')
                     sliceKeyE = recebe.index('=')
                     outro_chaveE = recebe[3:sliceKeyE]
                      
                     sliceKeyN = recebe.index('+')
                     outro_chaveN = recebe[sliceKeyE+1:sliceKeyN]
                     print('Chaves Recebidas E {}, N {}'.format(outro_chaveE,outro_chaveN))

                     sliceName = recebe.index('*')
                     self.nomeOutro = recebe[sliceKeyN+1:sliceName]
                     print('Nome : ', self.nomeOutro)
                     
                 else :
                     recebe = recebe.split('_')

                     recebeInt = []
                     codificadoRsaRecebimento = []
                     preCodificadoRecebimento = []

                     for i in  recebe:
                         aux0 = int(i)
                         recebeInt.append(aux0)
                         print(recebeInt)  #                        
                      
                    # -- Decodificacao
                     for i in recebeInt:
                         aux1 = (i ** minha_chaveD) % minha_chaveN
                         codificadoRsaRecebimento.append(aux1)
                         print(codificadoRsaRecebimento)  #
                         
                    # -- des pré Codificação
                     for i in codificadoRsaRecebimento:
                         aux2 = alfabeto[i // 10]
                         preCodificadoRecebimento.append(aux2)
                         print(preCodificadoRecebimento)   #

                    # -- Reajuntando a mensagem
                     mensagemOriginal = ''.join(preCodificadoRecebimento)
                     print('Mensagem Original : ', mensagemOriginal.capitalize())                     
               
                     # Após recebimento, exibe na tela o conteúdo da mensagem decriptografado 
                     labelMessage2 = Label(self.frame, text=mensagemOriginal.capitalize(), anchor=W, wraplength=200, bg="#B0C4DE", width=63)
                     labelMessage2.pack(fill="both", padx=5, pady=10, ipadx=5, ipady=10)  
        # ************************************************
        ''' Iniciando o Thread responsável por executar a função recebimento '''
        funcao1 = Thread (target=recebeMensagem) 
        funcao1.start()        
        # ************************************************
        # ************************************************
        ''' Evento, ao pressionar 'Enter', pelo Entry da tela inicial '''
        def avancar(event):   
            enviarChaves()
            print('Tentativas : ', contx)
        
            print('Avancar')      
            self.frameUm_nome.pack_forget()

            # Frame exibe o nome do outro usuário
            self.frameNome = Frame(master, bg ="#4682B4")                                                     # Frame Show his name
            self.frameNome.pack(side=TOP, fill="both")

            # Label que receberá nome do outro usuário
            self.lbNomeOutro = Label(self.frameNome, text="Nome Outro", bg="#B0C4DE")
            self.lbNomeOutro.pack(fill=X, pady=5)

            # Exibe mensagens
            self.frameShowMessage = Frame(master, bg="#B0C4DE", relief=FLAT)             # Show Message
            self.frameShowMessage.pack(side=TOP, fill="both")

            # Após receber nome, o coloca na label 'lbNomeOutro'
            self.lbNomeOutro["text"] = self.nomeOutro
            # ************************************************
            ''' Enviar mensagens, após 'Enter' pressionado pelo Entry da tela de envio '''
            def enviarMensagens(event):
                global outro_chaveE, outro_chaveN

                # Mensagem
                x = self.message.get().lower()
                print(x)       

                # Mostrar  
                labelMessage = Label(self.frame, text=x.capitalize(), anchor=E, wraplength=200, bg="#4682B4", width=63)
                labelMessage.pack(fill="both", padx=5, pady=10, ipadx=10, ipady=10)

                try:
                    print('Enviando')                   
                    ip = '192.168.15.2'
                    port = 2121
                    add = (ip, port)           
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    clientSocket.connect(add)

                    # Chaves
                    outro_chaveE = int(outro_chaveE)
                    outro_chaveN = int(outro_chaveN)                                  
      
                     # Pré Cifragem   
                    preCodificadoEnvio = []      
                    codificadoRsaEnvio = []
                    codificadoRsaStringEnvio = []
           
                    for i in x:
                       aux3 = alfabeto.index(i) * 10
                       preCodificadoEnvio.append(aux3)

                    # Cifragem
                    for i in preCodificadoEnvio:
                       aux4 = (i ** outro_chaveE) % outro_chaveN
                       codificadoRsaEnvio.append(aux4)

                    for i in codificadoRsaEnvio:
                       aux5 = str(i)
                       codificadoRsaStringEnvio.append(aux5)
          
                    codificadoRsaEnvio = '_'.join(codificadoRsaStringEnvio)    

                    print("Enviando ... ")
                    clientSocket.sendto(codificadoRsaEnvio.encode(), (ip, port))                    
                    self.message.delete(0, END)
                except ConnectionRefusedError:
                    print("Não foi possivel enviar sua mensagem")

                self.message.delete(0, END)      
            # ************************************************                                              Comando Scroolbar
            ''' Comando Scrollbar, após rolagem '''
            def myfunction(event):
                canvas.configure(scrollregion=canvas.bbox("all"),width=550,height=470, bg="#B0C4DE")                
            # ************************************************                                              Scroolbar           
            self.myframe=Frame(master,relief=FLAT, bg="#B0C4DE")
            self.myframe.pack()         
        
            canvas=Canvas(self.myframe,width=550,height=470, bg="#B0C4DE")
            self.frame=Frame(canvas, bg="#B0C4DE")
            myscrollbar=Scrollbar(self.myframe,orient="vertical",command=canvas.yview, bg="#B0C4DE")
            canvas.configure(yscrollcommand=myscrollbar.set)

            myscrollbar.pack(side="right",fill="y")
            canvas.pack(side="left")
            canvas.create_window((0,0),window=self.frame,anchor=NW)
            self.frame.bind("<Configure>",myfunction)    
            # ************************************************
            # Mensagem aos usuários
            self.labelMessage = Label(self.frameShowMessage, text="Sessão de chat criptografado ponta a ponta", wraplength=250, bg="#87CEFA")
            self.labelMessage.pack(fill=X, padx=5, pady=10, ipadx=5, ipady=10)

            # Frame com Entry
            self.frameShowInput = Frame(master, bg="#B0C4DE")                         # Show Input 
            self.frameShowInput.pack(side=BOTTOM, fill="both")

            # Entry - para digitação
            self.message = Entry(self.frameShowInput, borderwidth=0, insertbackground="lightgray", bg="#4682B4")
            self.message.focus_set()
            self.message.bind("<Return>", enviarMensagens)
            self.message.pack(fill=X, padx=20, pady=10)
        # ************************************************                                                  Widgets Tela 1          
        # Nome
        self.frameUm_nome = Frame(master, bg="#87CEEB")                                            # Frame Um_nome                                                                                                              
        self.frameUm_nome.pack(fill="both", pady=250)

        # Label
        self.lb1 = Label(self.frameUm_nome, text = "Open : "+ horario() + ' s', anchor=W, fg="#fff", bg="#87CEEB")
        self.lb1.pack(fill=X)
        self.lb2 = Label(self.frameUm_nome, text = "Nome : ", anchor=W, fg="#fff", bg="#87CEEB")
        self.lb2.pack(fill=X, padx=150)

        # Entry
        self.ed2 = Entry(self.frameUm_nome, width=30, borderwidth=0, insertbackground="lightgray", bg="#87CEEB", fg="#fff")
        self.ed2.focus_set()
        self.ed2.bind("<Return>", avancar)
        self.ed2.pack(pady=5)

root = Tk()
root.geometry("550x620+250+80")
root.configure(background="#4682B4")
Aplicacao(root)
root.mainloop()
