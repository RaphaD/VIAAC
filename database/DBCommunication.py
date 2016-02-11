import sqlite3

__author__ = 'fums'


class DBCommunication(object):
    def __init__(self, dbLocation):
        self._db = sqlite3.connect(dbLocation)

    def getOrderToSend(self, order):
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
        res = curs.fetchall()
        curs.close()
        return res

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
        curs.close()
        return result

    def setState(self, toUpdate):
        column = toUpdate.split()[0]
        newValue = ""
        sqlRequest = ""
        try:
            newValue = int(toUpdate.split()[1])
            sqlRequest = """
                    UPDATE StateNumber
                    SET State = ?
                    WHERE StateName = ?;
                     """
        except ValueError:
            newValue = toUpdate.split()[1]
            sqlRequest = """
                    UPDATE StateString
                    SET State = ?
                    WHERE StateName = ?;
                     """
        finally:
            curs = self._db.cursor()
            curs.execute(sqlRequest, (newValue, column,))
            self._db.commit()
            curs.close()

    def getState(self, toQuery):
        curs = self._db.cursor()
        sqlRequest = """
        SELECT State
        FROM StateNumber
        WHERE StateName = ?
        UNION
        SELECT State
        FROM StateString
        WHERE StateName = ?;
        """
        curs.execute(sqlRequest, (toQuery, toQuery))
        result = curs.fetchall()
        curs.close()
        return result
