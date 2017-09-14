import sys
import socket
import pickle
import time
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
    SinPort = 0
    SoutPort = 0
    CSinport = 0
    packetCount = 0
    
    Sin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSout
    StoC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSin
    
   
    
    StoC.bind(("127.0.0.1",7001))
    StoC.connect(("127.0.0.1",5000))
    
    Sin.bind(("127.0.0.1",5089))
    Sin.connect(("127.0.0.1",5001))
    
    Sin.setblocking(0)
    StoC.setblocking(0)
    #StoC.connect()
    
    
    #testpack = Packet(0x497E,0,0,0,"")
    
    
    
   
    
    print("test")
    
    pieceSize = 512
    message = []
    ####################"rb" on linux "r" on windows?????
    with open("in.txt", "r") as inFile:
        while True:
            piece = inFile.read(pieceSize)
            message.append(piece)
            print(piece)
            
            if piece == "":
                break
    inFile.close()
    print(message)
    
    exitFlag = False
    nextt = 0
    packetBuffer = []
    while(not exitFlag):
        
        toSendMsg = message.pop(nextt)
        lengthMsg = len(toSendMsg)
        if lengthMsg == 0:
            packet = Packet(0x497E,0,nextt,0,"")
            packetBuffer.append(packet)
            exitFlag = True
        else:
            print("in else")
            packet = Packet(0x497E,1,nextt,lengthMsg,toSendMsg)
            packetBuffer.append(packet)
            #prepare normal packet
            
        
        if(len(packetBuffer) != 0):
            (print("test2"))
            temp = packetBuffer.pop(0)
            i=0
            while(i<5):
                print(i)
                i+=1
                try:
                    data = Sin.recv(1024)
                    recv = pickle.loads(data)
                    if(not checkPacket(recv)):
                        raise
                    if(pickle.loads(data).typeField == 0):
                        raise ackPacket
                #except EOFError:
                    
                    ##Runs when the reciever has closed
                    #print("transfer completed with packets: " + str(packetCount))
                    #Sin.close()
                    #StoC.close() 
                    #return 0
                      
                except packetError:
                    print("packet error found")
                    print("############")
                    
                    
                except ackPacket:
                    print("acknowledgement packet recieved")
                    i = 10
                    data = Sin.recv(1024)
                    #runs when the packet is acknowledgement type
                    
                except:
                    #handle not the right ackPacket
                    StoC.send(pickle.dumps(temp))
                    time.sleep(0.2)
                    packetCount += 1
                    
                #while(pickle.loads(data) != Packet(0x497E,0,rcvd.seqno,0,"") ):
                    #packetCount+= 1
                    #StoC.send(pickle.dumps(packetBuffer.pop(0)))
                    #time.sleep(0.2) #Works, but need a concrete value                
               
    print("transfer completed with packets: " + str(packetCount))            
    Sin.close()
    StoC.close()     
    
        ##new loop
        ##send out packet increase packet counter
        ##wait for response
        ##if response complete checks
        ##if checks pass increment next go to outerloop
        ##else restart loop
    
main()