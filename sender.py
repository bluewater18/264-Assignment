import sys
import socket
import pickle
from packet import Packet




def main():
    Sin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSout
    StoC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSin
    
    StoC.bind(("127.0.0.1",7001))
    StoC.connect(("127.0.0.1",5000))
    
    
    Sin.connect(("127.0.0.1",5001))
    #StoC.connect()
    
    
    pack = Packet(0x497E,0,0,0,"")
    StoC.send(pickle.dumps(pack))
    
    
    Sin.close()
    StoC.close()    
    
    sys.exit()
    
    #pieceSize = 512
    #message = []
    #with open("in.txt", "rb") as inFile:
        #while True:
            #piece = inFile.read(pieceSize)
            #message.append(piece)
            
            #if piece == "":
                #break
    #print(message)
    
    #exitFlag = False
    #nextt = 0
    #packetBuffer = []
    
    #while(not exitFlag):
        #toSendMsg = message.get(nextt)
        #lengthMsg = len(toSendMsg)
        #if lengthMsg == 0:
            #packet = packet(0x497E,0,nextt,0,"")
            ##pickle
            #packetBuffer.append(packet)
            
            #pass
        #else:
            #packet = packet(0x497E,0,nextt,lengthMsg,toSendMsg)
            #packetBuffer.append(packet)
            ##prepare normal packet
            #pass
        
    
    
        ##new loop
        ##send out packet increase packet counter
        ##wait for response
        ##if response complete checks
        ##if checks pass increment next go to outerloop
        ##else restart loop
    
main()