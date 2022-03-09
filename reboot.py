# Dean Ralph
# 05/03/2022
#
# Project Title: Reboot hanler
# Current Version: 1
#
# Short Description: handles the rebooting
#
# Initialisation:
import sqlHandle
import paramiko

# Global Variables: 
sqlConnection = sqlHandle.SQL()

invokeRebootCommand = "sudo reboot"

# Functions:
def invokeReboot(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(invokeRebootCommand)
    line = stdout.readline()
    return line

# Main Code:
if __name__ == "__main__":
    serverList = sqlConnection.getRebootStatus()

    for x in serverList:
        print(f"Checking {x[0]}")
        if x[2] == 1 and x[3] == 0:
            serverUsername = sqlConnection.getUsername(x[0])[0]
            serverPassword = sqlConnection.getPassword(x[0])[0]
            rebootReq = invokeReboot(x[1], 22, serverUsername, serverPassword)
            for line in rebootReq:
                print(line)
            sqlConnection.updateRebootStatus(x[0], 0)
        else:
            print("No reboot required")