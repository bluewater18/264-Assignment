import sys, select, socket, pickle, random
from packet import Packet

def checkPort(port):
    if(port>1024 and port < 64000):
        return True
    return False

def checkProb(prob):
    if(prob>=0 and prob<=1):
        return True
    return False


def main():
    if (len(sys.argv) != 8):
        print("Not all arguments entered")
        return 0    
    try:
        for x in range(1,7):
            sys.argv[x] = int(sys.argv[x])
        sys.argv[-1] = float(sys.argv[-1])
    except:
        print("arguments not correctly formatted")
    for port in sys.argv[1:-2]:
        if(not checkPort(port)):
            print("Ports must be in range 1024 - 64000")
            return 0
    if(not checkProb(sys.argv[7])):
        print("probability needs to be in range [0-1]")
        return 0
    #Testing Values
    CSinPort = sys.argv[1]
    CSoutPort = sys.argv[2]
    CRinPort = sys.argv[3]
    CRoutPort = sys.argv[4]
    SinPort = sys.argv[5]
    RinPort = sys.argv[6]
    probability = sys.argv[7]
    
    
    #Socket Creation
    try:
        CRin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CRin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        CRin.setblocking(0)
        CRin.bind(("127.0.0.1",CRinPort))
        CRin.listen(1)
    except:
        print("Error in CRin Socket")
        return 0
    try:
        CRout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CRout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        CRout.setblocking(0)
        CRout.bind(("127.0.0.1",CRoutPort))
        CRout.listen(1) 
    except:
        print("Error in CRout Socket")
        return 0        
    try:
        CSin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CSin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        CSin.setblocking(0)
        CSin.bind(("127.0.0.1",CSinPort))
        CSin.listen(1) 
    except:
        print("Error in CSin Socket")
        return 0    
    
    try:
        CSout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CSout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        CSout.setblocking(0)
        CSout.bind(("127.0.0.1",CSoutPort))
        CSout.listen(1)     
    except:
        print("Error in CSout Socket")
        return 0
    
    
    #Socket Organisation
    inList = [CRin, CRout, CSin, CSout]
    outList = []
    StoC = None
    RtoC = None
    CtoR = None
    CtoS = None
    connList = [StoC, RtoC, CtoR, CtoS]
    
    
    while inList:
        readable, writable, exceptional = select.select(inList,outList, inList)
        for s in readable:
            if s in [CRin, CRout, CSin, CSout]:
                conn, addr = s.accept()
                conn.setblocking(0)
                #print(conn)
                inList.append(conn)
                if (addr == ("127.0.0.1",SinPort)):
                    StoC = conn
                    
                if (addr == ("127.0.0.1",RinPort)):
                    RtoC = conn
                    
                if (addr == ("127.0.0.1", 5069)):
                    CtoR = conn
                    
                if (addr == ("127.0.0.1", 5089)):
                    CtoS = conn
                    
                print("new connection from" + str(addr))
            #The afforementioned sockets [CRin, CRout, CSin, CSout] are no longer useable to distinguish after they have completed connection
            else:
                data=s.recv(1024)
                
                if data:                 
                    if s == RtoC: #From Reciever
                        
                        try:
                            temp = pickle.loads(data)
                            if(not introduceErrors(data, probability)):
                                try:
                                    CtoS.send(pickle.dumps(temp))
                                    
                                except:
                                    
                                    for s in readable + writable + exceptional:
                                        s.shutdown(socket.SHUT_RDWR)
                                        s.close()
                        except:
                            pass
                        
                    if s == StoC: #From Sender
                        
                        temp = pickle.loads(data)
                        if(not introduceErrors(temp,probability)):
                            try:
                                CtoR.send(pickle.dumps(temp))
                            except:
                                
                                for s in readable + writable + exceptional:
                                    s.shutdown(socket.SHUT_RDWR)
                                    s.close() 
                                                                
                                return 0
                            
                        #temp.printPacket()
                        pass
                    #add data to msg
                    if s not in outList:
                        outList.append(s)
                else:
                    if s in outList:
                        outList.remove(s)
                    inList.remove(s)
                    s.close()
                        #destroy msg

 

def introduceErrors(packet, probability):
    if random.uniform(0,1) < probability:
        #packet dropped
        return True
    else:
        bitError(packet)
        return False

def bitError(packet):
    """uses uniform distribution between 0 and 1. if this < 0.1 will increment dataLen by random num between 0-10"""
    #random.seed(555)
    if random.uniform(0,1) < 0.1:
        #bit error introduced
        packet.dataLen += int(random.uniform(0,10))


main()