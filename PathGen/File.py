import math
import Convert
import Point
import Transfer
import glob
import json
from paramiko import SSHClient
import paramiko
from scp import SCPClient

class File:

    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def uploadFile(self, localFilePath):
        self.scp.put(localFilePath, remote_path='/home/lvuser/deploy')
        self.scp.close()

    def connect(self):
        try:
            self.ssh.connect('10.44.99.2', username='lvuser', password='', timeout=1)
            self.scp = SCPClient(self.ssh.get_transport())
            return True
        except TimeoutError:
            print('Timeout Error')
            return False
        except:
            pass

    def uploadAll(self):
        saves = glob.glob("json-paths/*.json*")
        for save in saves:
            self.scp.put(save, remote_path='/home/lvuser/deploy')

    def downloadAll(self):
        sftp = self.ssh.open_sftp()
        files = sftp.listdir('/home/lvuser/deploy')
        print(str(files))
        for f in files:
            if f.endswith('.json'):
                self.scp.get(remote_path='/home/lvuser/deploy/' + f, local_path='json-paths/')
        
    def getListFromJSON(self, jsonObject):
        returnList = []
        with open(jsonObject) as jsonList:
            for i in range(0, len(jsonList)):
                returnList.append(jsonList[i])
        return returnList

    def getSave(self, fileName, fieldWidth, fieldHeight):
        saves = glob.glob("json-paths/*.json*")
        for save in saves:
            if fileName in save:
                with open(save) as jsonSave:
                    data = json.load(jsonSave)
                    newPoints = []
                    for x in range(len(data)):
                        newPoints.append(Point.Point(data[x]["x"], data[x]["y"], fieldWidth, fieldHeight, data[x]["angle"], data[x]["speed"], data[x]["time"], data[x]["deltaTime"], data[x]["interpolationRange"], data[x]["color"]))
                    for x in range(len(newPoints)):
                        newPoints[x].index = x
                Point.setPoints(newPoints)
                #print(save)
                return save
        return None
