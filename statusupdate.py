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

# Initialisation:
if len(sys.argv) != 3:
    sys.exit("Incorrect CLI arguments, please use statusupdate.py followed by the server name and 1 for true/0 for false")

# Global Variables: 
serverName = sys.argv[1]
rebootStatus = sys.argv[2]

# Main:
if __name__ == "__main__":
    print (f"Updateing status on: {serverName} to {rebootStatus}")
    con = pymysql.connect(host="192.168.0.209", port=3306, user="dean", password="Sackboy123", db=f"patching")
    cur = con.cursor()
    cur.execute(f"UPDATE `patching`.`rebootStatus` SET `rebootReq` = {int(rebootStatus)} WHERE `serverName` = '{serverName}';")
    con.commit()