import sys
import socket
import pickle
import time
from packet import Packet

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
    Sin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    StoC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSin
    StoC.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
   
    
    StoC.bind(("127.0.0.1",7001))
    StoC.connect(("127.0.0.1",5000))
    
    Sin.bind(("127.0.0.1",5089))
    Sin.connect(("127.0.0.1",5001))
    
    Sin.setblocking(0)
    
    pieceSize = 512
    message = []
    with open("in.txt", "r") as inFile:
        while True:
            piece = inFile.read(pieceSize)
            message.append(piece)
            print(piece)
            
            if piece == "":
                break
    inFile.close()
    print(message)
    #testfile = open("test.txt","w")
    
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

            
        
        if(len(packetBuffer) != 0):
            (print("test2"))
            temp = packetBuffer.pop(0)
            while(True):
                try:
                    data = Sin.recv(1024)
                    recv = pickle.loads(data)
                    print("current Packet")
                    print(str(recv.dataLen))
                    print("****")
                    if(not checkPacket(recv)):
                        raise packetError
        
                    if(recv.typeField == 0):
                        print("ak Packet")
                        break  
                except EOFError:
                    #Runs when the reciever has closed
                    print("transfer completed with packets: " + str(packetCount))
                    shutdown(Sin)
                    shutdown(StoC)                    
                    Sin.close()
                    StoC.close() 
                    return 0
                
                except:
                    #handle not the right ackPacket
                    StoC.send(pickle.dumps(temp))
                    
                    packetCount += 1
                    
                finally:
                    time.sleep(0.1)            
    Sins.shutdown(socket.SHUT_RDWR)
    StoCs.shutdown(socket.SHUT_RDWR)
    Sin.close()
    StoC.close()     
    
main()