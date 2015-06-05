import socket

from VIAACClient import VIAACClient


__author__ = 'fums'


class VIAACServer(object):
    def __init__(self, arduino, portServer, clientTreshold):
        self._port = portServer
        self._arduino = arduino
        self._isServerRunning = True

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(('', self._port))
        self._sock.listen(clientTreshold)

        print "Server started on port " + str(self._port)

    def mainLoop(self):

        clients = []

        while self._isServerRunning:
            # Accepter connexion
            clientConnection, connectionInfo = self._sock.accept()
            print "New client", connectionInfo

            # Start client thread
            Client = VIAACClient(socket=clientConnection, clientInfo=connectionInfo, arduino=self._arduino)
            Client.start()

            clients.append(Client)

        for client in clients:
            client.join()


if __name__ == '__main__':
    arduino = None
    port = 9002
    clientTreshold = 5
    VS = VIAACServer(arduino=arduino, portServer=port, clientTreshold=clientTreshold)
    VS.mainLoop()