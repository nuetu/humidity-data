import datetime
import re
import time
import json
from pyvesync import VeSync
import password

data_file = "/data/"

def writeToFile(a,b,c,d,e): #time, outdoor humidity, outdoor temperature, indoor humidity, indoor temperature, mist power level
    file = open("/data/humidity_data.csv", "a")
    line = "{},{},{},{},{}\n".format(a,b,c,d,e)
    file.write(line)
    file.close()

def getDate(dateFormat): #format the date to specific formats
    rn = datetime.datetime.now()
    if dateFormat == "sheets":
        return rn.strftime("%Y.%m.%d %H:%M")
    elif dateFormat == "day":
        return rn.strftime("%Y-%m-%d")
    elif dateFormat == "hour":
        return rn.strftime("%H:00:00")

def dataMap(line): 
    time = re.split('T|\+00:00/PT',line["validTime"])
    if (time[0] == getDate("day")):
        time.append(line["value"])
        return time
    else:
        pass
    
def parseJSON(fileName):
    file = data_file + fileName + ".json"
    with open(file) as f:
        data = json.load(f)
    #unit = data[0]["uom"].split(':')[1]
    values = data[0]["values"]
    values = map(dataMap, values)
    todayValues = []
    for i in values:
        if i != None:
            print(i)
            todayValues.append(i)
    return(todayValues)

def findCurrentValue(fileName):
    todayList = parseJSON(fileName)
    currentValue = -1
    for i in todayList:
        if (i[1] == getDate("hour") and int(i[2][0]) == 1):
            currentValue = round(int(i[3]),2)
        elif (int(getDate("hour")[:2]) == (int(i[1][:2]) + int(i[2][0]) -1) and currentValue == -1):
            currentValue = round(int(i[3]),2)
    return currentValue

account = VeSync(password.email, password.password, debug=False) #log in with user email and user password to VeSync 
account.login()
account.update()
my_humidifier = account.fans[0] #this may change depending on the amount of VeSync products in the account

while (my_humidifier.details["mist_virtual_level"] > 0): #while humidifier is not off 
    account.update()
    my_humidifier = account.fans[0]
    date = getDate("sheets")
    humidity = findCurrentValue("humidity")
    temperature = findCurrentValue("temperature")
    indoor_humidity = my_humidifier.details["humidity"]
    power_level = my_humidifier.details["mist_virtual_level"]
    writeToFile(date,humidity,temperature,indoor_humidity,power_level)
    print("CSV Updated")
    time.sleep(300) #wait 5 minutes 
