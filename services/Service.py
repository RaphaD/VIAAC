from speaking.VoiceAnalyzer import VoiceAnalyzer
from utils.params import FLAG_RAW_COMMAND, FLAG_GET_STATE, FLAG_SET_STATE_RAW_COMMAND


class Service:
    def __init__(self, request, client, database, socket, voicer):
        self._request = request
        self._clientInfo = client
        self._toSend = None
        self._db = database
        self._socket = socket
        self._voicer = voicer

    def treatRequest(self):
        # Direct raw command
        if FLAG_RAW_COMMAND in self._request:
            self.rawCommandCheck()
        # Raw command plus update value
        elif FLAG_SET_STATE_RAW_COMMAND in self._request:
            self.rawSetStateCheck()
        # Get state command
        elif FLAG_GET_STATE in self._request:
            self.stateCheck()
        # Spoken message to interpret
        else:
            self.voiceCheck()

        return self._toSend

    def rawCommandCheck(self):
        print "RAW_COMMAND"
        data = self._request.split()[1:]
        toQuery = ""
        for i in range(len(data)):
            if i != 0:
                toQuery += " " + data[i]
            else:
                toQuery += data[i]
        print "Message from : ", self._clientInfo
        print toQuery
        self._toSend = self._db.getOrderToSend(toQuery)
        print "Fetched from db : ", self._toSend

    def rawSetStateCheck(self):
        print "RAW_COMMAND"
        data = self._request.split()[1:]
        toQuery = ""
        for i in range(len(data)):
            if i != 0:
                toQuery += " " + data[i]
            else:
                toQuery += data[i]
        print "Message from : ", self._clientInfo
        print toQuery
        self._toSend = self._db.getOrderToSend(toQuery)
        self._db.setState(toQuery)

    def stateCheck(self):
        print "FLAG_GET_STATE"
        data = self._request.split()[1:]
        if len(data) == 1:
            state = self._db.getState(data[0])
            self._socket.send(str(state[0][0]) + "\n")

    def voiceCheck(self):
        print "VOICE_CASE"
        Analyze = VoiceAnalyzer(data=self._request, voicer=self._voicer)
        Analyze.main()
        self._toSend = Analyze.getResult()
