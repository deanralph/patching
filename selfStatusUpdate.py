# Dean Ralph
# 05/03/2022
#
# Project Title: Reboot Status update
# Current Version: 1
#
# Short Description: Updates the status on the reboot requoired table
#
# Imports:
import pymysql
import sys
import socket


# Initialisation:
if len(sys.argv) != 2:
    sys.exit("Incorrect CLI arguments, please use statusupdate.py followed by 1 for true/0 for false")

# Global Variables: 
serverName = socket.gethostname()
rebootStatus = sys.argv[1]

# Main:
if __name__ == "__main__":
    print (f"Updateing status on: {serverName} to {rebootStatus}")
    con = pymysql.connect(host="192.168.0.209", port=3306, user="dean", password="Sackboy123", db=f"patching")
    cur = con.cursor()
    cur.execute(f"UPDATE `patching`.`rebootStatus` SET `rebootReq` = {int(rebootStatus)} WHERE `serverName` = '{serverName}';")
    con.commit()