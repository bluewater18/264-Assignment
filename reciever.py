import sys, socket, pickle, time
from packet import Packet


def checkPacket(packet):
    if (packet.checksum != sum([packet.magnico,packet.typeField,packet.seqno,packet.dataLen])):
        return False
    return True

def main():
    RinPort = 3001
    RoutPort = 3000
    CRinPort = 6000
    filename = "out.txt"
    packetCount = 0
    
    Rin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CRout
    Rout = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CRin
    #Rin = socket.socket()
    #Rin.setblocking(0)
    '''Try except block in case the port is already binded'''
    #try:
        
    Rin.bind(("127.0.0.1",5069))
    Rout.bind(("127.0.0.1",7000))
    #except:
        #print("You haven't closed the program!!!\nExit")
        #return 0;
    
    Rin.connect(("127.0.0.1",RinPort))
    Rout.connect(("127.0.0.1",RoutPort))
    #Rout.connect(("127.0.0.1",CRinPort))
    
    #opening file
    writeDest = open(filename, "w")
    
    expected = 0
    
    data = Rin.recv(1024)
    while data:
        rcvd = pickle.loads(data)
        rcvd.printPacket()
        
        if(rcvd.typeField == 0):#Final Packet from Sender
            print("Terminating Packet - Break out of code")
            print("packets sent :" + str(packetCount))
            break
        
        if(rcvd.magnico == 0x497E and rcvd.typeField):
            print("Recieved Packet")
            
            #Need to check packet for error somewhere
            if(checkPacket(rcvd)):
                #Packet is good
                writeDest.write(rcvd.data)
                
                if(rcvd.seqno == expected):
                    ackPacket = Packet(0x497E,0,rcvd.seqno,0,"")
                    try:
                        data = Sin.recv(1024)
                        
                        
                        
                    except:   
                        print("error")
                        #while(not data):
                        print("Sending")
                        packetCount += 1
                        Rout.send(pickle.dumps(ackPacket))#send acknowledgement packet
                        time.sleep(0.1)#Wait for next packet
                        data = Rin.recv(1024)#load the next datasegment
                        
                else:
                    #writeDest.write(rcvd.data)
                    print("Invalid packet")
                    break
            else:
                data = Rin.recv(1024)
        
                
        
    writeDest.close()
    Rin.close()
    Rout.close()
    print("cleaned up")
    
    
main()