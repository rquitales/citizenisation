import time, sys, random, json, csv
from collections import defaultdict
from kafka import KafkaProducer, KeyedProducer

#Define Argument variables for readability.
sensorTopic = "testTopic"
ipFile = 'ipAddresses.txt'
seedFile = "/home/rquitales/git/Insight/Challenge/groupData/output/concat.txt"

#Function to format new seed data entries into defaultdict structure.
def insertEntry(dictionary, deviceID, latitude, longitude, value):
    dictionary[str(deviceID)]["latitude"] = latitude
    dictionary[str(deviceID)]["longitude"] = longitude
    dictionary[str(deviceID)]["value"] = value

#Function to read unique number of lines in seed data file.
def createSeedData(filename, numOfDevices = 100000):
    seedData = defaultdict(dict)
    with open(filename, 'r') as csvfile:
        d_id = 1
        for row in csv.DictReader(csvfile):
            insertEntry(seedData, d_id, row['Latitude'], row['Longitude'], float(row['Values']))
            d_id += 1
            if d_id > numOfDevices:
                break
    return seedData

#Modify seed data's sensor value for randomisations/simulations.
def modifyReading(dictionary):
    for device in dictionary:
        dictionary[device]['value'] = dictionary[device]['value'] + random.randint(-5,5)

#Send data to kafka.
def send2Kafka(ipAddresses, data, deviceKey):
    kProducer = (KafkaProducer(bootstrap_servers = ipAddresses,
              value_serializer = lambda v: json.dumps(v).encode('utf-8')))
    kProducer.send(sensorTopic, {deviceKey: [data[deviceKey]['latitude'], data[deviceKey]['longitude'], data[deviceKey]['value']]})

def main():
    #Create seed data.
    seedData = createSeedData(seedFile, 100000)
    #Get Kafka IP addressesself.
    ipAddresses = open(ipFile, 'r')
    ip = ipAddresses.read()
    ipAddresses.close()
    ip = ip.split(",")
    for devKey in seedData.keys():
        send2Kafka(ip, seedData, devKey)
    #for devKey in seedData.keys():
    #    print({deviceKey: [seedData[deviceKey]['latitude'], seedData[deviceKey]['longitude'], seedData[deviceKey]['value']]})
    i = 0
    while i < 10:
        modifyReading(seedData)
        for devKey in seedData.keys():
            send2Kafka(ip, seedData, devKey)
        #for j in seedData.keys():
        #    print(seedData[j])
        i += 1
        time.sleep(1)

if __name__ == "__main__":
  main()
