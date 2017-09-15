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

Sin = None
Sout = None

def freeSockets():
    try:
        Sin.shutdown(socket.SHUT_RDWR)
        Sout.shutdown(socket.SHUT_RDWR)
        Sin.close()
        Sout.close()   
    except:
        pass
    
def main():
    
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
        
    
    SinPort = sys.argv[1]
    SoutPort = sys.argv[2]
    CSinPort = sys.argv[3]
    filename = sys.argv[4]
    
    if(not os.path.isfile("./"+filename)):
        print("File Does Not Exist")
        return 0     
    
    packetCount = 0
    try:
        Sin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSout
        Sin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        StoC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects to CSin
        StoC.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        print("Error Making Ports")
        freeSockets()
        return 0
   
    try:
        StoC.bind(("127.0.0.1",7001))    
        Sin.bind(("127.0.0.1",SinPort))
    except:
        print("Error Binding ports")
        freeSockets()
        return 0
        
    try:
        StoC.connect(("127.0.0.1",SoutPort))
        Sin.connect(("127.0.0.1",CSinPort))
    except:
        print("Error Connecting Ports")
        freeSockets()
        return 0
    
    Sin.setblocking(0)
    
    pieceSize = 512
    message = []
    
    
    with open(filename, "r") as inFile:
        while True:
            piece = inFile.read(pieceSize)
            message.append(piece)
            
            
            if piece == "":
                break
    inFile.close()
    
    
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
            packet = Packet(0x497E,1,nextt,lengthMsg,toSendMsg)
            packetBuffer.append(packet)

            
        
        if(len(packetBuffer) != 0):
            temp = packetBuffer.pop(0)
            while(True):
                try:
                    data = Sin.recv(1024)
                    recv = pickle.loads(data)
                    if(not checkPacket(recv)):
                        raise packetError
        
                    if(recv.typeField == 0):
                        #acknowledgement package recieved
                        break  
                except EOFError:
                    #Runs when the reciever has closed
                    print("transfer completed with packets: " + str(packetCount))
                    freeSockets()
                    return 0
                
                except:
                    #handle not the right ackPacket
                    StoC.send(pickle.dumps(temp))
                    
                    packetCount += 1
                    
                finally:
                    time.sleep(0.1)  
                    
    freeSockets()   
    
main()