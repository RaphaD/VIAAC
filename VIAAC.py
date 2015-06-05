from server.VIAACServer import VIAACServer
from local.VIAACVoice import VIAACVoice

__author__ = 'fums'

# Some variables needed for the server initialisation
PORT_SERVER = 9004  # Opened port
CLIENT_TRESHOLD = 5  # Same-time connections

# Some variables needed for the arduino communication initialisation
USB_PORT = "/dev/ttyACM0"
BAUDRATE = 9600


class VIAAC(object):
    def __init__(self):
        # Initialisation of the server
        self.initArduinoCommunication()

    def initProcesses(self):
        print "Initialisation of the different services"
        self._voicer = VIAACVoice()
        self._server = VIAACServer(self._arduino, PORT_SERVER, CLIENT_TRESHOLD)

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