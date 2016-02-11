from database.DBCommunication import DBCommunication

__author__ = 'fums'


class VoiceAnalyzer(object):
    def __init__(self, data, voicer):
        self._voicer = voicer
        self._data = data
        self._db = DBCommunication("VIAACdb.db")
        self._result = None

    def preTreatment(self):
        print self._data
        self._data = self._data.lower()
        # Watch out for non-ASCII ?

    def searchAssociatedSentece(self):
        lookLikeSentence = {}
        for word in self._data.split():
            fetched = self._db.getLikeInBehaviour(word)
            for tuple in fetched:
                lookLikeFetched = tuple[0]
                moreOpsFetched = tuple[1]
                if lookLikeFetched in lookLikeSentence:
                    lookLikeSentence[lookLikeFetched][0] += 1
                else:
                    lookLikeSentence[lookLikeFetched] = [1, moreOpsFetched]

        matchList = []
        for key in lookLikeSentence.keys():
            if len(key.split()) == lookLikeSentence[key][0]:
                matchList.append((key, lookLikeSentence[key][1]))

        print "matchList", matchList
        if len(matchList) == 1:
            return matchList[0][0], matchList[0][1]
        else:
            return None, None

    def getAssociatedFiles(self, match):
        allWordsInSentence = self._db.getFileListToPlay(match)
        return allWordsInSentence

    def postTreatment(self, match):
        if match == "what time date":
            self.makeDate()
            self.makeTime()
        elif match == "what time":
            self.makeTime()
        elif match == "which date":
            self.makeDate()

    def sendToVoicer(self, fileList):
        print fileList
        l = []
        for i in range(len(fileList)):
            l.append(str(fileList[i][0]))
        self._voicer.addToSay(l)

    def main(self):
        self.preTreatment()
        match, resultRequiresMoreOps = self.searchAssociatedSentece()
        if match:
            fileList = self.getAssociatedFiles(match)
            if resultRequiresMoreOps:
                self.postTreatment(match)
            self.sendToVoicer(fileList)

    def getResult(self):
        return self._result


"""
if __name__ == "__main__":
    VV = VIAACVoice()
    VV.start()

    VA = VoiceAnalyzer("who are you", VV)
    VA.main()

    # VA = VoiceAnalyzer("count to ten", VV)
    #    VA.main()

    VA = VoiceAnalyzer("hello my name is sean", VV)
    VA.main()

    VA = VoiceAnalyzer("hello my name is raphael", VV)
    VA.main()
    """
