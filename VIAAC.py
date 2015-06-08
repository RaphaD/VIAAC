from server.VIAACServer import VIAACServer
from utils.VIAACVoice import VIAACVoice
from utils.params import PORT_SERVER, CLIENT_TRESHOLD

__author__ = 'fums'


class VIAAC(object):
    def __init__(self):
        # Initialisation of the server
        self.initArduinoCommunication()

    def initProcesses(self):
        print "Initialisation of the different services"
        self._voicer = VIAACVoice()
        self._server = VIAACServer(arduino=self._arduino, voicer=self._voicer,
                                   portServer=PORT_SERVER, clientTreshold=CLIENT_TRESHOLD)

    def startProcesses(self):
        self._server.mainLoop()
        self._voicer.mainLoop()

    def initArduinoCommunication(self):
        # self._arduino = ArduinoCommunication(USB_PORT, BAUDRATE)
        self._arduino = None


if __name__ == "__main__":
    V = VIAAC()
    V.initProcesses()
    V.startProcesses()
    V.startProcesses()