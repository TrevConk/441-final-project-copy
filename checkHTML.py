location = '/usr/lib/cgi-bin/pinData.txt'
import json
import time



def checkHTML():
  with open(location, 'r') as pinDataRead:
            pinData = json.load(pinDataRead)
            state = pinData['selection']
            secretCode = pinData['pin']
            print(state)
            # Three different possible states
            # 'Turn Off Alarm' -> disables alarm
            # 'Arm Alarm' -> sensing
            # 'Reset Pin' -> changes pin

def updateHTML(state):
  dataDump = {'pin':secretCode,'selection':state}
  with open(location, 'w') as f:
    json.dump(dataDump, f)
            # Three different possible states
            # 'Turn Off Alarm' -> disables alarm
            # 'Arm Alarm' -> sensing
            # 'Reset Pin' -> changes pin

while True:
  checkHTML()
  time.sleep(2)