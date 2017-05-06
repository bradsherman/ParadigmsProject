from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor
from main import GameSpace
import cPickle as pickle


class Server(object):

    def __init__(self):
        self.commandPort1 = 9000
        self.dataPort1 = 9002
        self.player2DataQueue = DeferredQueue()

    def run(self):
        reactor.listenTCP(self.commandPort1, ServerCommandConnectionFactory(self))
        reactor.run()

class ServerCommandConnection(Protocol):
    def __init__(self, server):
        self.server = server

    def connectionMade(self):
        print "Command connection established"
        self.transport.write("start data connection")
        reactor.listenTCP(self.server.dataPort1, ServerDataConnectionFactory(self.server))

    def dataReceived(self, data):
        pass

class ServerDataConnection(Protocol):
    def __init__(self, server):
        self.server = server
        self.paddlex = 0
        self.paddley = 0

    def connectionMade(self):
        print "Data connection established"
        self.server.player2DataQueue.get().addCallback(self.updatePos)
        # start the game
        try:
            print "starting player 1"
            gs = GameSpace(self, 1)
            gs.run()
        except:
            return

    def dataReceived(self, data):
        self.server.player2DataQueue.put(data)

    def updatePos(self, data):
        # print "data: ", data
        try:
            pos = pickle.loads(data)
            self.paddlex = pos["paddlex"]
            self.paddley = pos["paddley"]
            self.server.player2DataQueue.get().addCallback(self.updatePos)
        except:
            print "Couldn't parse data"
            self.server.player2DataQueue.get().addCallback(self.updatePos)
            pass


class ServerDataConnectionFactory(Factory):
    def __init__(self, server):
        self.server = server
        self.myconn = ServerDataConnection(self.server)

    def buildProtocol(self, addr):
        return self.myconn

class ServerCommandConnectionFactory(Factory):
    def __init__(self, server):
        self.server = server
        self.myconn = ServerCommandConnection(self.server)

    def buildProtocol(self, addr):
        return self.myconn

if __name__ == "__main__":
    server = Server()
    server.run()
