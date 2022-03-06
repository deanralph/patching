# Dean Ralph
# 05/03/2022
#
# Project Title: Main Patching Script
# Current Version: 1
#
# Short Description: Patches Ubuntu boxes and updated the reboot required table
#
# Initialisation:
import pymysql
import paramiko
import json

with open("/jenkins/patching/dbConn.json", "r") as f:
    dbConn = json.load(f)

con = pymysql.connect(host=dbConn["server"], port=3306, user=dbConn["user"], password=dbConn["password"], db=dbConn["database"])

# Global Variables: 
getRebootCommand = """if [ -f /var/run/reboot-required ]; 
  then
    echo '1'
  else
    echo '0'
fi"""

getUpdateCommand = """sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt autoclean -y"""

rebooServerCommand = "sudo reboot"

# Functions
def updateDB(serverName, status):
    print (f"Updateing status on: {serverName} to {status}")
    cur = con.cursor()
    cur.execute(f"UPDATE `patching`.`rebootStatus` SET `rebootReq` = {int(status)} WHERE `serverName` = '{serverName}';")
    con.commit()

def getServerList():
    print (f"Getting server list")
    cur = con.cursor()
    cur.execute("SELECT * FROM patching.serverDetails;")
    rows = cur.fetchall()  
    return rows

def checkForReboot(host, port, username, password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        stdin, stdout, stderr = ssh.exec_command(getRebootCommand)
        line = stdout.readline()
        return line

def runUpdates(host, port, username, password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        stdin, stdout, stderr = ssh.exec_command(getUpdateCommand)
        lines = stdout.readlines()
        return lines

def rebootSSH(host, port, username, password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        stdin, stdout, stderr = ssh.exec_command(rebooServerCommand)
        lines = stdout.readlines()
        return line

# Main:
if __name__ == "__main__":
    serverList = getServerList()
    
    for server in serverList:
        print(server[1])
        if server[5] != 1:
            update = runUpdates(server[2], 22, server[3], server[4])
            for line in update:
                print(line)
        rebootReq = checkForReboot(server[2], 22, server[3], server[4])
        print(rebootReq[0])
        updateDB(server[1], int(rebootReq[0]))
        if rebootReq[0] == "1":
            rebootSSH(server[2], 22, server[3], server[4])
            rebootConfirm = updateDB(server[1], 0)
