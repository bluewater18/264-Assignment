import sys
import socket
import pickle
import time
from packet import Packet

def main():
    SinPort = 0
    SoutPort = 0
    CSinport = 0
    
    Sin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSout
    StoC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSin
    
    StoC.bind(("127.0.0.1",7001))
    StoC.connect(("127.0.0.1",5000))
    
    
    Sin.connect(("127.0.0.1",5001))
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
            print("in if")
            packet = Packet(0x497E,0,nextt,0,"")
            #pickle
            packetBuffer.append(packet)
            exitFlag = True
        else:
            print("in else")
            packet = Packet(0x497E,0,nextt,lengthMsg,toSendMsg)
            packetBuffer.append(packet)
            #prepare normal packet
            
        
        if(len(packetBuffer) != 0):
            StoC.send(pickle.dumps(packetBuffer.pop(0)))
            time.sleep(0.5) #Works, but need a concrete value
        
    Sin.close()
    StoC.close()     
    
        ##new loop
        ##send out packet increase packet counter
        ##wait for response
        ##if response complete checks
        ##if checks pass increment next go to outerloop
        ##else restart loop
    
main()