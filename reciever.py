import sys, socket, packet, pickle



def main():
    RinPort = 3001
    RoutPort = 3000
    CRinPort = 6000
    filename = "out.txt"
    
    Rin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CRout
    #Rout = socket.socket() #connects to CRin
    #Rin = socket.socket()
    #Rin.setblocking(0)
    '''Try except block in case the port is already binded'''
    try:
        Rin.bind(("127.0.0.1",5069))
    except:
        print("You haven't closed the program!!!\nExit")
        return 0;
    
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
        if(rcvd.magnico == 0x497E and rcvd.typeField):
            print("Recieved Packet")
            if(rcvd.seqno == expected):
                ackPacket = Packet(0x497E,'acknowledgementPacket',rcvd.seqno,0,)#send acknowledgement packet
            else:
                writeDest.write(rcvd.data)
                print("Invalid packet")
                break
        data = Rin.recv(1024)#load the next datasegment
                
        
    writeDest.close()
    Rin.close()
    #Rout.close()
    
    
main()