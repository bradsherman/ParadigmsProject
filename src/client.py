from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from main import GameSpace
import json

class Client(object):
    def __init__(self):
        self.server_host = '10.18.12.41'
        self.commandPort = 9000
        self.dataPort = 9002
	self.player1DataQueue = DeferredQueue()

    def run(self):
        reactor.connectTCP(self.server_host, self.commandPort, ClientCommandConnectionFactory(self))
        reactor.run()

class ClientCommandConnectionFactory(ClientFactory):
    def __init__(self, client):
        self.myconn = ClientCommandConnection(client)

    def buildProtocol(self, addr):
        return self.myconn

class ClientCommandConnection(Protocol):
    def __init__(self, client):
        self.client = client

    def connectionMade(self):
        pass

    def dataReceived(self, data):
        if data == 'start data connection':
            reactor.connectTCP(self.client.server_host, self.client.dataPort, ClientDataConnectionFactory(self.client))

class ClientDataConnectionFactory(ClientFactory):
    def __init__(self, client):
        self.myconn = ClientDataConnection(client)

    def buildProtocol(self, addr):
        return self.myconn

class ClientDataConnection(Protocol):
    def __init__(self, client):
	self.client = client
	self.paddlex = 0
	self.paddley = 0

    def connectionMade(self):
        self.client.player1DataQueue.get().addCallback(self.updatePos)
        try:
            print 'starting player 2'
            gs = GameSpace(self, 2)
            gs.run()
        except:
            return

    def dataReceived(self, data):
	print "data: ", data
	self.client.player1DataQueue.put(data)
        pass
    
    def updatePos(self, data):
        print "data: ", data
	try:
	    pos = json.loads(data)
	    if "paddlex" in pos.keys():
		self.paddlex = pos["paddlex"]
		self.paddley = pos["paddley"]
	    if "ballx" in pos.keys():
		self.ballx = pos["ballx"]
		self.bally = pos["bally"]
	    self.client.player1DataQueue.get().addCallback(self.updatePos)
	except:
	    print 'could not parse data'
	    self.client.player1DataQueue.get().addCallback(self.updatePos)
	    pass


if __name__ == "__main__":
    client = Client()
    client.run()
