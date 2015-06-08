import sqlite3

__author__ = 'fums'


class DatabaseUpdater(object):
    def __init__(self):
        self._db = sqlite3.connect('VIAACdb.db')

    def getAllRequests(self):
        curs = self._db.cursor()
        sqlRequest = """
        SELECT id, FullAnswer
        FROM Requests;
        """
        curs.execute(sqlRequest)
        answers = curs.fetchall()
        curs.close()
        return answers

    def searchWord(self, word):
        curs = self._db.cursor()
        sqlRequest = """
        SELECT id
        FROM Words
        WHERE Words.Word = ?
        """
        curs.execute(sqlRequest, (word, ))
        return curs.fetchone()

    def update(self):
        answers = self.getAllRequests()
        curs = self._db.cursor()
        for answer in answers:
            answerId = answer[0]
            splittedAnswer = answer[1].split()
            for i in range(len(splittedAnswer)):
                wordId = self.searchWord(splittedAnswer[i])[0]
                self.insertInLink(curs, answerId, wordId, i)
        self._db.commit()
        curs.close()
        self._db.close()

    def insertInLink(self, curs, answerId, wordId, wordPlace):
        sqlRequest = """
        INSERT INTO AnswerWordLinks (WordPlace, RequestId, WordId)
        VALUES (?, ?, ?);
        """
        curs.execute(sqlRequest, (wordPlace, answerId, wordId,))


if __name__ == "__main__":
    UD = DatabaseUpdater()
    UD.update()