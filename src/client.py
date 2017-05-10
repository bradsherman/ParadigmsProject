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
        self.server_host = '10.18.162.207'
        self.commandPort = 9000
        self.dataPort = 9002
        self.player1DataQueue = DeferredQueue()
        self.player1OutgoingDataQueue = DeferredQueue()

    def run(self):
	# Create connection with server
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

    def connectionMade(self):
        print "data connection established"
        self.client.player1DataQueue.get().addCallback(self.updatePos)
        self.client.player1OutgoingDataQueue.get().addCallback(self.toServer)
        try:
	    # Starting player 2
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
                #print "shutting down"
                self.shutdown()
            if "paddle1x" in pos.keys():
                self.gs.paddle1.update(pos["paddle1x"], pos["paddle1y"]) 
	    if "paddle2x" in pos.keys():
                self.gs.paddle2.update(pos["paddle2x"], pos["paddle2y"]) 
            if "ball" in pos.keys():
                self.gs.ball.update(pos["ball"]["ballx"], pos["ball"]["bally"], pos["ball"]["ballspeedx"], pos["ball"]["ballspeedy"])
            if "bricks" in pos.keys():
		bricks_hp = pos["bricks"]
		for brick in self.gs.bricks:
		    if brick.id in bricks_hp.keys():
			brick.hp = bricks_hp[brick.id]
		    else:
			brick.hp = 0
		[brick.update() for brick in self.gs.bricks]
            self.client.player1DataQueue.get().addCallback(self.updatePos)
        except:
            print 'could not parse data:', pos
            self.client.player1DataQueue.get().addCallback(self.updatePos)

    def toServer(self, data):
	# Callback function for sending data to server
        self.transport.write(data)
        self.client.player1OutgoingDataQueue.get().addCallback(self.toServer)

    def connectionLost(self, reason):
        self.shutdown()

    def shutdown(self):
	# Stops game and quits
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
