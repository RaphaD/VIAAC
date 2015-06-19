import threading
import time

from pydub import AudioSegment
from pydub.playback import play


__author__ = 'fums'


class VIAACVoice(threading.Thread):
    def __init__(self):
        super(VIAACVoice, self).__init__()
        self._WAIT_TIME = 2
        self._toSay = []
        self._waitForSay = True

    def run(self):
        while self._waitForSay:
            if not (len(self._toSay) == 0):
                print "Should say something"
                sentence = self._toSay.pop(0)
                self.say(sentence)
            else:
                time.sleep(self._WAIT_TIME)

    def addToSay(self, element):
        self._toSay.append(element)

    def say(self, sentence):
        print "say method"
        fullSentence = AudioSegment.from_mp3(sentence[0])
        for i in range(1, len(sentence)):
            print "sentence[i] ", sentence[i]
            wordToPlay = AudioSegment.from_mp3(sentence[i])
            fullSentence += wordToPlay
        print "Ready to play"
        play(fullSentence)