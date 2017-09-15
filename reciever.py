import sys, socket, pickle, time, os
from packet import Packet


def checkPacket(packet):
    if (packet.checksum != sum([packet.magnico,packet.typeField,packet.seqno,packet.dataLen])):
        return False
    return True

def checkPort(port):
    if(port>1024 and port < 64000):
        return True
    return False

Rin = None
Rout = None

def freeSockets():
    try:
        Rin.shutdown(socket.SHUT_RDWR)
        Rout.shutdown(socket.SHUT_RDWR)
        Rin.close()
        Rout.close()    
    except:
        pass

def main():
    '''Reciever program. Recieves data from sender through channel
    storing this is the file provided'''
    if (len(sys.argv) != 5):
        print("Not all arguments entered")
        return 0
    try:
        for x in range(1,4):
            sys.argv[x] = int(sys.argv[x])
    except:
        print("arguments not correctly formatted")
        
    for port in sys.argv[1:4]:
        if(not checkPort(port)):
            print("Ports must be in range 1024 - 64000")
            return 0
        
         
    RinPort = sys.argv[1]
    RoutPort = sys.argv[2]
    CRinPort = sys.argv[3]
    filename = sys.argv[4]
    packetCount = 0
    
    if(os.path.isfile("./"+filename)):
        print("File Already Exists")
        return 0       
    
    try:
        Rin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CRout
        Rin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Rout = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CRin
        Rout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        print("Error making sockets")
        freeSockets()
        return 0

    try:
        Rin.bind(("127.0.0.1",5069))
        Rout.bind(("127.0.0.1",7000))
    except:
        print("Error binding sockets")
        freeSockets()
        return 0
    
    try:
        Rin.connect(("127.0.0.1",RinPort))
        Rout.connect(("127.0.0.1",RoutPort))
    except:
        print("Error Connecting Sockets")
        freeSockets()
        return 0
    #except:
        #print("Error connecting sockets")
        #return 0
    
    #opening file
    
   
    writeDest = open(filename, "w")
    expected = 0
    
    
    data = Rin.recv(1024)
    while data:
        rcvd = pickle.loads(data)
        
        
        if(rcvd.typeField == 0):#Final Packet from Sender
            print("packets sent :" + str(packetCount))
            break
        
        if(rcvd.magnico == 0x497E and rcvd.typeField):
            #packed recieved
            
            #Need to check packet for error somewhere
            if(checkPacket(rcvd)):
                #Packet is good
                writeDest.write(rcvd.data)
                
                if(rcvd.seqno == expected):
                    ackPacket = Packet(0x497E,0,rcvd.seqno,0,"")

                        

                    #sending
                    packetCount += 1
                    Rout.send(pickle.dumps(ackPacket))#send acknowledgement packet
                    time.sleep(0.1)#Wait for next packet
                    data = Rin.recv(1024)#load the next datasegment
                        
                else:
                    #invalid packet
                    break
            else:
                data = Rin.recv(1024)
        
                
    #cleanup   
    writeDest.close()
    freeSockets()
    
    
    
main()