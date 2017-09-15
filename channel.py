import sys, select, socket, pickle, random
from packet import Packet




def main():
    
    #Testing Values
    CSinPort = 5000
    CSoutPort = 5001
    CRinPort = 3000
    CRoutPort = 3001
    SinPort = 7001
    RinPort = 7000
    probability = 0.0
    
    
    #Socket Creation
    CRin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    CRin.setblocking(0)
    
    CRin.bind(("127.0.0.1",CRinPort))
    CRin.listen(1)
    
    CRout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    CRout.setblocking(0)
    CRout.bind(("127.0.0.1",CRoutPort))
    CRout.listen(1) 
    
    
    CSin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    CSin.setblocking(0)
    CSin.bind(("127.0.0.1",CSinPort))
    CSin.listen(1) 
    
    CSout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    CSout.setblocking(0)
    CSout.bind(("127.0.0.1",CSoutPort))
    CSout.listen(1)     
    
    
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
                    print("StoC")
                if (addr == ("127.0.0.1",RinPort)):
                    RtoC = conn
                    print("RtoC")
                if (addr == ("127.0.0.1", 5069)):
                    CtoR = conn
                    print("CtoR")
                if (addr == ("127.0.0.1", 5089)):
                    CtoS = conn
                    print("CtoS")
                print("new connection from" + str(addr))
            #The afforementioned sockets [CRin, CRout, CSin, CSout] are no longer useable to distinguish after they have completed connection
            else:
                data=s.recv(1024)
                
                if data:
                    #print(s)
                    #temp = pickle.loads(data)
                    #temp.printPacket()                    
                    if s == RtoC: #From Reciever
                        print("CRin")
                        try:
                            temp = pickle.loads(data)
                            if(not introduceErrors(data, probability)):
                                try:
                                    CtoS.send(pickle.dumps(temp))
                                    print("Ctos")
                                except:
                                    print("closed")
                                    for s in readable + writeable + exceptional:
                                        s.shutdown(socket.SHUT_RDWR)
                                        s.close()
                        except:
                            pass
                        
                    if s == StoC: #From Sender
                        print("CSin")
                        temp = pickle.loads(data)
                        if(not introduceErrors(temp,probability)):
                            try:
                                CtoR.send(pickle.dumps(temp))
                            except:
                                print("closed")
                                for s in readable + writeable + exceptional:
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
        print("packet dropped")
        return True
    else:
        bitError(packet)
        return False

def bitError(packet):
    """uses uniform distribution between 0 and 1. if this < 0.1 will increment dataLen by random num between 0-10"""
    #random.seed(555)
    if random.uniform(0,1) < 0.1:
        print("bit error introduced")
        packet.dataLen += int(random.uniform(0,10))




    


main()