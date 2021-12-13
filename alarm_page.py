#!/usr/bin/python37all
import cgi
import cgitb
import json

#Setip for the creation of the new webpage
cgitb.enable(display=0, logdir="/home/pi/Documents/htmlissues")
data = cgi.FieldStorage()

#setting up the different variables
#  #received from the webpage
selection = data.getvalue('buttonHit')
if(selection == 'Reset Pin'):
    pin = data.getvalue('Enter New Pin')
else:
    with open('pinData.txt', 'r') as pinDataRead:
        pinData = json.load(pinDataRead)
        pin = pinData['pin']
dataDump = {'pin':pin,'selection':selection}
with open('pinData.txt', 'w') as f:
        json.dump(dataDump, f)

print('Content-type: text/html\n\n')
print('''
    <html>
    <form action="/cgi-bin/alarm_page.py" method="POST">
        <b>Alarm Control Page</b><br>
        <b>Turn Off Alarm</b><br>
        <input type="submit" name="buttonHit" value="Turn Off Alarm"><br>
        <b>Arm Alarm</b><br>
        <input type="submit" name="buttonHit" value="Arm Alarm"><br>
        <b>Reset Pin Password:</b><br>
        <input type="text" name="Enter New Pin"><br>
        <input type="submit" name="buttonHit" value="Reset Pin"><br>
</input>
</form>
</html>''')