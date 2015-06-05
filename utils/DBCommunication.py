import sqlite3

__author__ = 'fums'


class DBCommunication(object):
    def __init__(self):
        self._db = sqlite3.connect('VIAACdb.db')

    def getOrderToSend(self, order):
        curs = self._db.cursor()
        sqlRequest = """
            SELECT id
            FROM Commands
            WHERE Command = ?"""
        curs.execute(sqlRequest, (order, ))
        curs.close()
        sqlResult = curs.fetchone()
        if sqlResult:
            return int(sqlResult[0])
        else:
            return None

    def getSentenceToSay(self, question):
        curs = self._db.cursor()
        sqlRequest = """
            SELECT Path
            FROM Questions
                JOIN Words
                ON Words.id = Questions.id
            WHERE Questions.question = ?
            ORDERED BY SentenceId, SentenceOrder;
            """
        curs.execute(sqlRequest, (question, ))
        curs.close()
        print curs.fetchall()