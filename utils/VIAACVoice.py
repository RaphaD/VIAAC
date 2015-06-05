import threading
import time

from utils.DBCommunication import DBCommunication


__author__ = 'fums'


class VIAACVoice(threading.Thread):
    def __init__(self):
        super(VIAACVoice, self).__init__()
        self._WAIT_TIME = 2
        self._db = DBCommunication()
        self._toSay = []
        self._waitForSay = True

    def run(self):
        while self._waitForSay:
            if not (len(self._toSay) == 0):
                sentence = self._toSay.pop(0)
                self.say(sentence)
            else:
                time.sleep(self._WAIT_TIME)

    def addToToSay(self, element):
        self._toSay.append(element)

    def say(self, sentence):
        print "bla"


"""
if __name__ == "__main__":
    VV = VIAACVoice()
    VV.start()
    VV.addToToSay()
    VV.join()
"""