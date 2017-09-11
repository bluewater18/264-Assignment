import sys, select, socket, pickle, packet

def makeSocket(portNum):
    channel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #channel_socket.setblocking(0)
    #channel_socket .setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    channel_socket.bind(("127.0.0.1", portNum))
    channel_socket.listen(1)
    
    return channel_socket


def main():
    
    #Testing Values
    CSinPort = 5000
    CSoutPort = 5001
    CRinPort = 3000
    CRoutPort = 3001
    SinPort = 7001
    RinPort = 7000
    probability = 0.5
    
    
    #Socket Creation
    CRin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRin.setblocking(0)
    CRin.bind(("127.0.0.1",CRinPort))
    CRin.listen(1)
    
    CRout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRout.setblocking(0)
    CRout.bind(("127.0.0.1",CRoutPort))
    CRout.listen(1) 
    
    
    CSin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSin.setblocking(0)
    CSin.bind(("127.0.0.1",CSinPort))
    CSin.listen(1) 
    
    CSout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSout.setblocking(0)
    CSout.bind(("127.0.0.1",CSoutPort))
    CSout.listen(1)     
    
    
    #Socket Organisation
    inList = [CRin, CRout, CSin, CSout]
    outList = []
    StoC = None
    RtoC = None
    CtoR = None
    
    
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
                    print("Set")
                if (addr == ("127.0.0.1",RinPort)):
                    RtoC = conn
                if (addr == ("127.0.0.1", 5069)):
                    print("CtoR")
                    CtoR = conn
                #create holder for msg??
                print("new connection from" + str(addr))
            #The afforementioned sockets [CRin, CRout, CSin, CSout] are no longer useable to distinguish after they have completed connection
            else:
                data=s.recv(1024)
                
                if data:
                    #print(s)
                    #temp = pickle.loads(data)
                    #temp.printPacket()                    
                    if s is CRin:
                        print("CRin")
                        #input from Reciever
                        pass
                    if s == StoC:
                        print("CSin")
                        temp = pickle.loads(data)#error when packet is not send i.e. at the end
                        #if(not introduceErrors(data)):
                        CtoR.send(pickle.dumps(temp))#pipe error occuring??
                            #pass
                        #temp.printPacket()
                        #input from sender
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
        #to be implemented
        return True
    else:
        bitError(packet)
        return False

def bitError(packet):
    """uses uniform distribution between 0 and 1. if this < 0.1 will increment dataLen by random num between 0-10"""
    random.seed(555)
    if random.uniform(0,1) < 0.1:
        packet.dataLen += int(random.uniform(0,10))



#Packet dumping and writing unused ATM    
def writePacket(_socket, packet):
    f = _socket.makefile('wb', 1024 )
    pickle.dump(packet, f, pickle.HIGHEST_PROTOCOL)
    f.close()

def readPacket(_socket):
    f = _socket.makefile('rb', buffer_size )
    data = pickle.load(f)
    f.close()
    return data
    


main()