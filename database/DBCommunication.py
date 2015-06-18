import sqlite3

__author__ = 'fums'


class DBCommunication(object):
    def __init__(self, dbLocation):
        self._db = sqlite3.connect(dbLocation)

    def getOrderToSend(self, order):
        print order
        print len(order)
        curs = self._db.cursor()
        sqlRequest = """
            SELECT id
            FROM Commands
            WHERE Command = ?"""
        curs.execute(sqlRequest, (order, ))
        sqlResult = curs.fetchone()
        curs.close()
        if sqlResult:
            return int(sqlResult[0])
        else:
            return None

    def getSentenceToSay(self, question):
        curs = self._db.cursor()
        sqlRequest = """
            SELECT PathTo
            FROM Questions
                JOIN Words
                ON Words.id = Questions.id
            WHERE Questions.question = ?
            ORDERED BY SentenceId, SentenceOrder;
            """
        curs.execute(sqlRequest, (question, ))
        curs.close()

    def getLikeInBehaviour(self, toCompare):
        toLookLike = "%" + toCompare + "%"
        curs = self._db.cursor()
        print toLookLike
        sqlRequest = """
            SELECT ToLookLike, MoreOperations
            FROM AvailableAnswers
            WHERE ToLookLike LIKE ?;
            """
        curs.execute(sqlRequest, (toLookLike, ))
        return curs.fetchall()

    def getFileListToPlay(self, match):
        curs = self._db.cursor()
        sqlRequest = """
                SELECT PathTo FROM (
                    Words JOIN (
                        AnswerWordLinks JOIN (
                            Answers JOIN
                                AvailableAnswers
                            ON Answers.id = AvailableAnswers.AnswerId)
                        ON AnswerWordLinks.AnswerId = Answers.Id)
                    ON Words.id = AnswerWordLinks.WordId)
                WHERE AvailableAnswers.ToLookLike = ?
                ORDER BY AnswerWordLinks.Wordplace;
                """
        curs.execute(sqlRequest, (match, ))
        result = curs.fetchall()
        return result