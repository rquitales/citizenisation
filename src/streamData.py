import time, sys, random, json, csv
from collections import defaultdict
from datetime import datetime
from kafka import KafkaProducer, KeyedProducer

#Define Argument variables for readability.
#sensorTopic = "iotData"
#ipFile = '../input/ipAddresses.txt'
#seedFile = "../input/japanSafecast.txt"
#sensorType = 'radiation'
#positionInFile = 1

sensorTopic = sys.argv[1]
ipFile = sys.argv[2]
seedFile = sys.argv[3]
sensorType = sys.argv[4]
positionInFile = int(sys.argv[5])

#Function to format new seed data entries into defaultdict structure.
def insertEntry(dictionary, deviceID, latitude, longitude, value):
    dictionary[str(deviceID)] = {'latitude': latitude, 'longitude' : longitude, 'value' : value, 'ctime' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

#Function to read unique number of lines in seed data file.
def createSeedData(filename, numOfDevices = 100, start = 1):
    seedData = {}
    with open(filename, 'r') as csvfile:
        rowPosition = 0
        d_id = 1
        for row in csv.DictReader(csvfile):
            rowPosition += 1
            if rowPosition < start:
                continue
            insertEntry(seedData, d_id, row['Latitude'], row['Longitude'], float(row['Values']))
            d_id += 1
            if (rowPosition - start) + 2 > numOfDevices:
                break
    return seedData

#Modify seed data's sensor value for randomisations/simulations.
def modifyReading(dictionary):
    for device in dictionary:
        dictionary[device]['value'] = dictionary[device]['value'] + random.randint(-5,5)
        dictionary[device]['ctime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#Send data to kafka.
def send2Kafka(ipAddresses, data, deviceKey, sensorType = 'radiation'):
    kProducer = (KafkaProducer(bootstrap_servers = ipAddresses,
              value_serializer = lambda v: json.dumps(v).encode('utf-8')))
    kProducer.send(sensorTopic, {sensorType: {'deviceID' : deviceKey, 'latitude' : data[deviceKey]['latitude'], 'longitude' : data[deviceKey]['longitude'], 'value' : data[deviceKey]['value'], 'ctime' : data[deviceKey]['ctime']}})
    kProducer.flush()

def main():
    #Create seed data.
    seedData = createSeedData(seedFile, numOfDevices = 100, start = positionInFile)
    #Get Kafka IP addressesself.
    ipAddresses = open(ipFile, 'r')
    ip = ipAddresses.read()
    ipAddresses.close()
    ip = ip.split(",")
    for devKey in seedData.keys():
        send2Kafka(ip, seedData, devKey, sensorType)
    i = 0
    while i < 10:
        modifyReading(seedData)
        for devKey in seedData.keys():
            send2Kafka(ip, seedData, devKey, sensorType)
        i += 1
        time.sleep(1)

if __name__ == "__main__":
  main()
