# Dean Ralph
# 05/03/2022
#
# Project Title: SQL Handeler
# Current Version: 1
#
# Short Description: handels the SQL connection
#
# Initialisation:
import pymysql
import json

with open("/jenkins/patching/dbConn.json", "r") as f:
    dbConn = json.load(f)

class SQL:
    def __init__(self):
        self.con = pymysql.connect(host=dbConn["server"], port=3306, user=dbConn["user"], password=dbConn["password"], db=dbConn["database"])

    def getServerList(self):
        cur = self.con.cursor()
        cur.execute(f"SELECT * FROM patching.serverDetails;")
        return cur.fetchall()

    def updateRebootStatus(self, serverName, status):
        cur = self.con.cursor()
        cur.execute(f"UPDATE `patching`.`rebootStatus` SET `rebootReq` = {int(status)} WHERE serverName = '{serverName}';")
        return cur.fetchone()

    def getRebootStatus(self):
        cur = self.con.cursor()
        cur.execute(f"SELECT * FROM patching.patchingStatus;")
        return cur.fetchall()

    def getUsername(self, serverName):
        cur = self.con.cursor()
        cur.execute(f"SELECT username FROM patching.serverDetails WHERE hostname = '{serverName}';")
        return cur.fetchone()

    def getPassword(self, serverName):
        cur = self.con.cursor()
        cur.execute(f"SELECT password FROM patching.serverDetails WHERE hostname = '{serverName}';")
        return cur.fetchone()