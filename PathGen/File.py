import math
import Convert
import Point
import Transfer
import glob
import json
from paramiko import SSHClient
import paramiko
from scp import SCPClient

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('10.44.99.2', username='lvuser', password='', timeout=1)
    scp = SCPClient(ssh.get_transport())
except TimeoutError:
    print('Timeout error')

def uploadFile(localFilePath):
    scp.put(localFilePath, remote_path='/home/lvuser/deploy')
    #scp.get('ExamplePath.json')

    #scp.put('test', recursive=True, remote_path='/home/user/dump')

    scp.close()

def uploadAll():
    saves = glob.glob("json-paths/*.json*")
    for save in saves:
        scp.put(save, remote_path='/home/lvuser/deploy')

def getSave(fileName, fieldWidth, fieldHeight):
    saves = glob.glob("json-paths/*.json*")
    for save in saves:
        if fileName in save:
            with open(save) as jsonSave:
                data = json.load(jsonSave)
                newPoints = []
                for x in range(len(data)):
                    newPoints.append(Point.Point(data[x]["x"], data[x]["y"], fieldWidth, fieldHeight, data[x]["angle"], data[x]["speed"], data[x]["time"], data[x]["color"]))
                for x in range(len(newPoints)):
                    newPoints[x].index = x
            Point.setPoints(newPoints)
            return save
    return None