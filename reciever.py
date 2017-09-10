import sys, socket, packet, pickle



def main():
    Rin = socket.socket() #connetx to CRout
    Rout = socket.socket() #connects to CRin
    Rin.connect(("127.0.0.1",3001))
    Rout.connect(("127.0.0.1",3000))
    
    data = Rin.recv(1024)
    while data:
        temp = pickle.loads(data)
        temp.printPacket()
        data = Rin.recv(1024)
                
        
    
    Rin.close()
    Rout.close()
    
   
    
main()