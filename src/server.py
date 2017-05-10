from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor
from main import GameSpace
import sys
import cPickle as pickle


class Server(object):

    def __init__(self):
        self.commandPort1 = 9000
        self.dataPort1 = 9002
        self.player2IncomingDataQueue = DeferredQueue()
        self.player2OutgoingDataQueue = DeferredQueue()

    def run(self):
        # Starts listening for client to connect
        reactor.listenTCP(self.commandPort1, ServerCommandConnectionFactory(self))
        reactor.run()

class ServerCommandConnection(Protocol):
    def __init__(self, server):
        self.server = server

    def connectionMade(self):
        # Command connection established
        # Tell server to connect on data port
        self.transport.write("start data connection")
        reactor.listenTCP(self.server.dataPort1, ServerDataConnectionFactory(self.server))

    def dataReceived(self, data):
        if data == 'player 2 ready':
            # print "player 2 ready"
            self.server.gs.add_player()

class ServerDataConnection(Protocol):
    def __init__(self, server):
        self.server = server

    def connectionMade(self):
        # print "Data connection established"
        self.server.player2IncomingDataQueue.get().addCallback(self.updatePos)
        self.server.player2OutgoingDataQueue.get().addCallback(self.toClient)
        # start the game
        try:
            # Start player 1
            self.gs = GameSpace(self, 1)
            self.gs.run()
        except:
            pass

    def dataReceived(self, data):
        self.server.player2IncomingDataQueue.put(data)

    def sendData(self, data):
        self.server.player2OutgoingDataQueue.put(data)

    def updatePos(self, data):
        try:
            # Process data over data connection
            pos = pickle.loads(data)
            if "winner" in pos.keys():
                self.gs.winner = pos["winner"]
            if "player2" in pos.keys():
                self.gs.add_player()
            if "shutdown" in pos.keys():
                # print "shutting down"
                self.shutdown()
            if "paddle2x" in pos.keys():
                self.gs.paddle2.update(pos["paddle2x"], pos["paddle2y"])
            self.server.player2IncomingDataQueue.get().addCallback(self.updatePos)
        except:
            print "Couldn't parse data", pickle.loads(data)
            self.server.player2IncomingDataQueue.get().addCallback(self.updatePos)

    def toClient(self, data):
        # Callback function to write data to client over data connection
        self.transport.write(data)
        self.server.player2OutgoingDataQueue.get().addCallback(self.toClient)

    def connectionLost(self, reason):
        self.shutdown()

    def shutdown(self):
        # Stops reactor and shuts down
        self.gs.other_exit()
        if reactor.running:
            reactor.stop()

    def shutdown_other(self):
        # Sends shutdown command to client
        req = {'shutdown': '1'}
        self.sendData(pickle.dumps(req))

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
