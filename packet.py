class Packet(object):
    """Class representation of packet. Expects hexa, 0 or 1, 0 or 1, int 0 - 512, data string of length of earlier int"""
    def __init__(self, magnico, typeField, seqno, dataLen, data):
        self.magnico = magnico
        self.typeField = typeField #True for normal False for acknowledgement
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data
        self.checksum = sum([magnico,typeField,seqno,dataLen]) 
        
    def printPacket(self):
        print(self.magnico)
        print(self.typeField)
        print(self.seqno)
        print(self.dataLen)
        print(self.data)
        
    
    #make a print method??
    