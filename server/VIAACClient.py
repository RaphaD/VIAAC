import socket
import time
from threading import Thread, RLock

from database.DBCommunication import DBCommunication
from services.Service import Service
from utils.params import MAX_CONNECTION_TIME, BUFFER_SIZE, SOCKET_TIMEOUT

__author__ = 'fums'


lock = RLock()


class VIAACClient(Thread):
    def __init__(self, socket, clientInfo, arduino, voicer):
        Thread.__init__(self)

        self._socket = socket
        self._socket.settimeout(SOCKET_TIMEOUT)
        self._clientInfo = clientInfo
        self._arduino = arduino
        self._voicer = voicer
        self._timer = time.time()
        self._listenToClient = True

    def run(self):
        db = DBCommunication("VIAACdb.db")

        while self._listenToClient:

            try:

                toSend = None
                data = self._socket.recv(BUFFER_SIZE)

                if data:
                    s = Service(data, self._clientInfo, db, self._socket, self._voicer)
                    toSend = s.treatRequest()

                    if toSend:
                        self._timer = time.time()
                        with lock:
                            # self._arduino.sendToIno(str(toSend) + ";")
                            print "sent to arduino : ", str(toSend) + ";"

                else:
                    self._socket.send("KEEP_ALIVE")

            except socket.timeout:
                self._listenToClient = not (time.time() - self._timer > MAX_CONNECTION_TIME)
            except socket.error:
                print "Client logged out"
                self._listenToClient = False
            else:
                self._listenToClient = not (time.time() - self._timer > MAX_CONNECTION_TIME)

        print "End of listening loop"
        try:
            self._socket.close()
        except:
            pass

    def setMustRun(self, mustRun):
        self._mustRun = mustRun

    def getSocket(self):
        return self._socket