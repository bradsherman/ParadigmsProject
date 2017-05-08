from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from main import GameSpace
import sys
import time
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
        print data
        if data == 'player 1 ready':
            print "player 1 ready"
            self.client.gs.add_player()
        elif data == 'start data connection':
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
        self.bricks = []

    def connectionMade(self):
        print "data connection established"
        self.client.player1DataQueue.get().addCallback(self.updatePos)
        self.client.player1OutgoingDataQueue.get().addCallback(self.toServer)
        try:
            print 'starting player 2'
            self.gs = GameSpace(self, 2)
            self.gs.run()
        except:
            pass

    def dataReceived(self, data):
        self.client.player1DataQueue.put(data)

    def sendData(self, data):
        self.client.player1OutgoingDataQueue.put(data)

    def updatePos(self, data):
        try:
            pos = pickle.loads(data)
            if "player1" in pos.keys():
                self.gs.add_player()
            if "shutdown" in pos.keys():
                print "shutting down"
                self.shutdown()
            if "paddle1x" in pos.keys():
                # print "updating paddle"
                self.gs.paddle1.update(pos["paddle1x"], pos["paddle1y"]) 
                self.gs.paddle2.update(pos["paddle2x"], pos["paddle2y"]) 
            if "ballx" in pos.keys():
                # print "updating ball"
		print "updating ball"
                self.gs.ball.update(pos["ballx"], pos["bally"], pos["ballspeedx"], pos["ballspeedy"])
            if "brick_id" in pos.keys():
                # self.bricks[pos["brick_id"]] = pos["brick_hp"]
                for b in self.bricks:
                    if b.id == pos["brick_id"]:
                        print "data: ", pos
                        print "updating brick " + str(b.id)
                        if "brick_hp" in pos:
                            b.hp = pos["brick_hp"]
                        else:
                            b.hp = 0
                # print "updated bricks"
                # print [str(b2.id) + " = " + str(b2.hp) for b2 in self.bricks]
            self.client.player1DataQueue.get().addCallback(self.updatePos)
        except:
            print 'could not parse data'
            self.client.player1DataQueue.get().addCallback(self.updatePos)

    def toServer(self, data):
        self.transport.write(data)
        self.client.player1OutgoingDataQueue.get().addCallback(self.toServer)

    def connectionLost(self, reason):
        self.shutdown()

    def shutdown(self):
        print "stopping reactor"
        self.gs.quit_game()
        reactor.stop()
        sys.exit()

    def shutdown_other(self):
        print "client data conn shutdown"
        req = {'shutdown': '1'}
        self.sendData(pickle.dumps(req))


if __name__ == "__main__":
    client = Client()
    client.run()
