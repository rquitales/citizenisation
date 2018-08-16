import time, random, csv, sys
from datetime import (datetime, timedelta)

logfile = "unique%s.txt"%(sys.argv[1])
filewriter = open("payload_air.txt", "w")
startTime = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

#Create specified number of datapoints per device
for iteration in range(1, int(sys.argv[2])):
    devID = 1
    #Do not modify reading for first row
    if iteration == 1:
        with open(logfile, 'r') as csvfile:
            for row in csv.DictReader(csvfile):
                line = '{"airquality": {"deviceID" : %s, "latitude" : %s, "longitude" : %s, "value" : %s, "ctime" : %s}}'%(devID, row['Latitude'], row['Longitude'], row['Values'], '"' + str(startTime) + '"') + "\n"
                filewriter.write(line)
                devID += 1
    #Create randomised values for further datapoints
    else:
        with open(logfile, 'r') as csvfile:
            for row in csv.DictReader(csvfile):
                line = '{"airquality": {"deviceID" : %s, "latitude" : %s, "longitude" : %s, "value" : %s, "ctime" : %s}}'%(devID, row['Latitude'], row['Longitude'], abs(float(row['Values']) + random.randint(-15,15)), '"' + str(startTime) + '"') + "\n"
                filewriter.write(line)
                devID += 1
    startTime += timedelta(seconds = 1)
    print("Iteration " + str(iteration) + " completed!")

filewriter.close()
