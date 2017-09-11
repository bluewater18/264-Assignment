import sys, socket, packet, pickle



def main():
    RinPort = 3000
    RoutPort = 3001
    CRinPort = 4000
    Rin = socket.socket() #connects to CRout
    Rout = socket.socket() #connects to CRin
    filename = "out.txt"
    
    Rin.connect(("127.0.0.1",RinPort))
    Rout.connect(("127.0.0.1",CRinPort))
    
    
    expected = 0
    
    data = Rin.recv(1024)
    while data:
        rcvd = pickle.loads(data)
        if(rcvd.magnico == 0x497E and rcvd.typeField):
            if(rcvd.seqno != expected):
                ackPacket = P
        temp.printPacket()
        data = Rin.recv(1024)
                
        
    
    Rin.close()
    Rout.close()
    
   
    
main()