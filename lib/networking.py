import socket , pickle , time
from random import randint


class connection():
    def __init__(self,conn=None):
        if conn == None :
            self.sock = socket.socket(socket.AF_INET)
        else :
            self.sock = conn
    
    def bind(self,**kwargs):
        self.server = True
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = randint(5000,9000)
        self.adress = (self.host,self.port)
        self.sock.bind((self.host,self.port))
        return self.adress

    def listen(self):
        # for recving conns from clients and some other shit
        if self.server != True:
            print("cant listen as not binded to an adress")
            return
        self.sock.listen(1)
        client_conn , addr = self.sock.accept()
        # make the clients conn into a network objct so that it can be used like that ykkkkkkkkkkkkkkkkk
        client_conn = connection(conn=client_conn)
        client_conn.server = False
        return (client_conn,addr)
    
    def connect(self,adress):
        # for clients so they can talk to servers
        self.server = False
        self.adress = adress
        self.sock.connect(adress)

    def send(self,msg,flag=""):
        # send messages yk 
        msg = pickle.dumps((msg,flag))
        self.sock.send(msg)
        time.sleep(0.01)
    
    def recv(self):
        # receive some messages (wish people would send me messages)
        Pmsg = b""
        msg = None
        while True :
            Pmsg += self.sock.recv(1024)
            loaded = True
            try: 
                msg = pickle.loads(Pmsg)
            except :
                loaded == False
            if loaded == True and msg != None:
                break
        return msg            

    def close(self):
        # if ur a server conect to ur self if ur in a listening loop or some shit and then DIE
        if self.server == True :
            try:
                tempSock = socket.socket(socket.AF_INET)
                tempSock.connect(self.adress)
                tempSock.close()
            except:
                pass
        self.sock.close()

