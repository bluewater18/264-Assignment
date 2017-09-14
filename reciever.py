import sys, socket, pickle, time
from packet import Packet



class Error(Exception):
    pass

class ackPacket(Error):
    pass

class packetError(Error):
    pass

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
    
    Rin.setblocking(0)
    Rout.setblocking(0)
    i = 0
    while i<10:
        i+= 1
        try:
            ackPacket = None
            data = Rin.recv(1024)
            rcvd = pickle.loads(data)
            rcvd.printPacket()
        
            if(rcvd.typeField == 0):#Final Packet from Sender
                print("Terminating Packet - Break out of code")
                print("packets sent :" + str(packetCount))
                break
        
            if(rcvd.magnico != 0x497E):
                print("Bad Packet")
                raise packetError
                
            if(not checkPacket(rcvd)):
                #Packet is good
                raise packetError
                #writeDest.write(rcvd.data)
                
            if(rcvd.seqno != expected):
                raise packetError
            #GOOD PACKET
            print("packet recieved")
            writeDest.write(rcvd.data)
            ackPacket = Packet(0x497E,0,rcvd.seqno,0,"")
            Rout.send(pickle.dumps(ackPacket))#send acknowledgement packet
            
            j = 0
            while j<3:
                j+=1
                try:
                    data = Rin.recv(1024)
                    recv = pickle.loads(data)
                except:
                    packetCount += 1
                    if ackPacket != None:
                        Rout.send(pickle.dumps(ackPacket))
                        
                    else:
                        j=100
                    time.sleep(0.2)
            
        except EOFError:
            time.sleep(0.2)
            
        except:
            print("in except")
            if ackPacket != None:
                print("sending ack packet")
                Rout.send(pickle.dumps(ackPacket))#send acknowledgement packet
                packetCount += 1
            time.sleep(0.2)#Wait for next packet
            #while j<10:
                #j+=1
                #try:
                    #data = Sin.recv(1024)
                #except:   
                    #print("error")
                    ##while(not data):
                    #print("Sending")
                    #packetCount += 1
                    #Rout.send(pickle.dumps(ackPacket))#send acknowledgement packet
                    #time.sleep(0.2)#Wait for next packet
                    ##data = Rin.recv(1024)#load the next datasegment
                    
            #else:
                #writeDest.write(rcvd.data)
                #print("Invalid packet")
                #break
        
                
        
    writeDest.close()
    Rin.close()
    Rout.close()
    print("cleaned up")
    
    
main()