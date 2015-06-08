import socket

from VIAACClient import VIAACClient


__author__ = 'fums'


class VIAACServer(object):
    def __init__(self, arduino, voicer, portServer, clientTreshold):
        self._port = portServer
        self._arduino = arduino
        self._voicer = voicer
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
            Client = VIAACClient(voicer=self._voicer, socket=clientConnection, clientInfo=connectionInfo,
                                 arduino=self._arduino)
            Client.start()

            clients.append(Client)

        for client in clients:
            client.join()