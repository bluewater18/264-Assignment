import sys, socket, packet, pickle



def main():
    RinPort = 3001
    RoutPort = 3000
    CRinPort = 6000
    filename = "out.txt"
    
    
    Rin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CRout
    #Rin = socket.socket()
    #Rin.setblocking(0)
    Rin.bind(("127.0.0.1",5069))
    #Rout = socket.socket() #connects to CRin
    
    
    Rin.connect(("127.0.0.1",RinPort))
    #Rout.connect(("127.0.0.1",CRinPort))
    
    
    
    
    #opening file
    writeDest = open(filename, "w")
    
    
    expected = 0
    
    data = Rin.recv(1024)
    while data:
        
        rcvd = pickle.loads(data)
        rcvd.printPacket()
        writeDest.write(rcvd.data)
        #if(rcvd.magnico == 0x497E and rcvd.typeField):
            #if(rcvd.seqno != expected):
                #ackPacket = Packet()#send acknowledgement packet
            #else:
                #writeDest.write(rcvd.data)
        data = Rin.recv(1024)#load the next datasegment
                
        
    writeDest.close()
    Rin.close()
    #Rout.close()
    
   
    
main()