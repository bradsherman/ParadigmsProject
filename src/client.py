from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from main import GameSpace
import cPickle as pickle

class Client(object):
    def __init__(self):
        self.server_host = '10.18.12.41'
        self.commandPort = 9000
        self.dataPort = 9002
        self.player1DataQueue = DeferredQueue()
        self.player1OutgoingDataQueue = DeferredQueue()

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
        self.ballx = 0
        self.bally = 0
        self.bricks = {}

    def connectionMade(self):
        self.client.player1DataQueue.get().addCallback(self.updatePos)
        self.client.player1OutgoingDataQueue.get().addCallback(self.toServer)
        try:
            print 'starting player 2'
            gs = GameSpace(self, 2)
            gs.run()
        except:
            return

    def dataReceived(self, data):
        self.client.player1DataQueue.put(data)

    def sendData(self, data):
        self.client.player1OutgoingDataQueue.put(data)

    def updatePos(self, data):
        try:
            pos = pickle.loads(data)
            print "data: ", pos
            if "paddlex" in pos.keys():
                print "updating paddle"
                self.paddlex = pos["paddlex"]
                self.paddley = pos["paddley"]
            if "ballx" in pos.keys():
                print "updating ball"
                self.ballx = pos["ballx"]
                self.bally = pos["bally"]
            if "brick_id" in pos.keys():
                self.brick_to_update = 1
                self.bricks[pos["brick_id"]] = pos["brick_hp"]
            self.client.player1DataQueue.get().addCallback(self.updatePos)
        except:
            print 'could not parse data'
            self.client.player1DataQueue.get().addCallback(self.updatePos)

    def toServer(self, data):
        self.transport.write(data)
        self.client.player1OutgoingDataQueue.get().addCallback(self.toServer)


if __name__ == "__main__":
    client = Client()
    client.run()
