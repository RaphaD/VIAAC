import socket
import time
from threading import Thread, RLock

from database.DBCommunication import DBCommunication
from speaking.VoiceAnalyzer import VoiceAnalyzer
from utils.params import MAX_CONNECTION_TIME, BUFFER_SIZE, SOCKET_TIMEOUT, FLAG_RAW_COMMAND, FLAG_GET_STATE

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
        self._db = DBCommunication("VIAACdb.db")

        while self._listenToClient:

            try:

                data = self._socket.recv(BUFFER_SIZE)

                if data:
                    toSend = None

                    # Direct raw command
                    if FLAG_RAW_COMMAND in data:
                        print "RAW_COMMAND"
                        data = data.split()[1:]
                        toQuery = ""
                        for i in range(len(data)):
                            if i != 0:
                                toQuery += " " + data[i]
                            else:
                                toQuery += data[i]
                        print "Message from : ", self._clientInfo
                        print toQuery
                        toSend = self._db.getOrderToSend(toQuery)
                        self._db.setState(toQuery)
                        print "Fetched from db : ", toSend

                    elif FLAG_GET_STATE in data:
                        print "FLAG_GET_STATE"
                        data = data.split()[1:]
                        if len(data) == 1:
                            state = self._db.getState(data[0])
                            self._socket.send(str(state[0][0]) + "\n")

                    # Spoken message to interpret
                    else:
                        Analyze = VoiceAnalyzer(data=data, voicer=self._voicer)
                        Analyze.main()
                        toSend = Analyze.getResult()
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