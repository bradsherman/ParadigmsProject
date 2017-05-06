from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from main import GameSpace

class Client(object):
    def __init__(self):
        self.server_host = '10.26.14.44'
        self.commandPort = 9000
        self.dataPort = 9002

    def run(self):
        reactor.connectTCP(self.server_host, self.commandPort, MyCommandConnectionFactory(self))
        reactor.run()

class MyCommandConnectionFactory(ClientFactory):
    def __init__(self, client):
        self.myconn = MyCommandConnection(client)

    def buildProtocol(self, addr):
        return self.myconn

class MyCommandConnection(Protocol):
    def __init__(self, client):
        self.client = client

    def connectionMade(self):
        pass

    def dataReceived(self, data):
        if data == 'start data connection':
            reactor.connectTCP(self.client.server_host, self.client.dataPort, MyDataConnectionFactory())

class MyDataConnectionFactory(ClientFactory):
    def __init__(self):
        self.myconn = MyDataConnection()

    def buildProtocol(self, addr):
        return self.myconn

class MyDataConnection(Protocol):
    def connectionMade(self):
        try:
            print 'starting player 2'
            gs = GameSpace(self, 2)
            gs.run()
        except:
            return

    def dataReceived(self, data):
        pass


if __name__ == "__main__":
    client = Client()
    client.run()
