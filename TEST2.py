from main.lib import networking
import threading

host = str(input("host>>"))
port =int(input("port>>"))
sock = networking.connection()
sock.connect((host,port))
sock.send("dan","nick")

def recv(sock):
    while True :
        print(sock.recv())

threading.Thread(target=recv,args=(sock,)).start()



