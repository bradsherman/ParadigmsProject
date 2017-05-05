from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor
from main import *


class Server(object):

    def __init__(self):
        # 10.18.8.119
        self.commandPort1 = 9000
        # self.commandPort2 = 9001
        self.dataPort1 = 9002
        # self.dataPort2 = 9003
        self.player2CommandQueue = DeferredQueue()
        self.player2DataQueue = DeferredQueue()

    def run(self):
        reactor.listenTCP(self.commandPort1, ServerCommandConnectionFactory(self))
        reactor.run()

class ServerCommandConnection(Protocol):
    def __init__(self, server):
        self.server = server

    def connectionMade(self):
        print "connection made!!"
        gs = GameSpace(self, 1)
        gs.main()
        return

    def dataReceived(self, data):
        if data == "start data connection":
            reactor.listenTCP(self.dataPort1, ServerDataConnectionFactory(self))

class ServerDataConnection(Protocol):
    def __init__(self, server):
        self.server = server

    def connectionMade(self):
        print "Data connection established"
        # start the game

    def dataReceived(self, data):
        print "data: ", data

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
