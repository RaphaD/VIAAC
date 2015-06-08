import threading
import time

from pydub import AudioSegment
from pydub.playback import play

from database import DBCommunication


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
        fullSentence = AudioSegment.from_mp3(sentence[0])
        for i in range(1, len(sentence)):
            wordToPlay = AudioSegment.from_mp3(sentence[i])
            fullSentence += wordToPlay
        play(fullSentence)

if __name__ == "__main__":
    VV = VIAACVoice()
    VV.start()
    VV.addToToSay(
        ["../voice/hello.mp3", "../voice/my.mp3", "../voice/name.mp3", "../voice/is.mp3", "../voice/VIAAC.mp3"])
    VV.join()