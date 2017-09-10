import sys, select, socket, pickle, packet

def makeSocket(portNum):
    channel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #channel_socket.setblocking(0)
    #channel_socket .setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    channel_socket.bind(("127.0.0.1", portNum))
    channel_socket.listen(1)
    
    return channel_socket
def main():
    CRin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRin.setblocking(0)
    CRin.bind(("127.0.0.1",3000))
    CRin.listen(1)
    
    CRout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRout.setblocking(0)
    CRout.bind(("127.0.0.1",3001))
    CRout.listen(1) 
    
    CSin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSin.setblocking(0)
    CSin.bind(("127.0.0.1",5000))
    CSin.listen(1) 
    
    CSout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSout.setblocking(0)
    CSout.bind(("127.0.0.1",5001))
    CSout.listen(1)     
    
    inList = [CRin, CRout, CSin, CSout]
    outList = []
    StoC = None
    RtoC = None
    
    
    while inList:
        readable, wratable, exceptional = select.select(inList,outList, inList)
        for s in readable:
            if s in [CRin, CRout, CSin, CSout]:
                conn, addr = s.accept()
                conn.setblocking(0)
                print(conn)
                inList.append(conn)
                if (addr == ("127.0.0.1",7001)):
                    StoC = conn
                    print("Set")
                if (addr == ("127.0.0.1",RtoC)):
                    RtoC = conn
                #create holder for msg??
                print("new connection from" + str(addr))
            #The afforementioned sockets [CRin, CRout, CSin, CSout] are no longer useable to distinguish after they have completed connection
            else:
                data=s.recv(1024)
                
                if data:
                    print(s)
                    #temp = pickle.loads(data)
                    #temp.printPacket()                    
                    if s is CRin:
                        print("CRin")
                        #input from Reciever
                        pass
                    if s == StoC:
                        print("CSin")
                        temp = pickle.loads(data)
                        temp.printPacket()
                        CRout.send(pickle.dumps(temp))
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