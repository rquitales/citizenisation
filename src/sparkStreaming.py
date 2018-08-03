from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
#from pyspark_cassandra import streaming
#import pyspark_cassandra,
import sys, json

from pyspark import StorageLevel

from pyspark.sql.functions import sum
from pyspark.sql.types import *
from pyspark.sql import Window
from pyspark.sql import SQLContext
from pyspark.sql import functions


def kafa2Json(sensorData):
  """ Parse input json stream """
  # The Kafka messages arrive as a tuple (None, {deviceKey: ['latitude', 'longitude', 'value']})
  # this first line grabs the nested json (second element)
  rawSensor = sensorData.map(lambda k: json.loads(k[1]))
  # .keys() finds all keys of the json - this case there is only one: "room"
  #return rawSensor.map(lambda x: json.loads(x[x.keys()[0]]))
  return rawSensor

def main():
    """ Joins two input streams to get location specidic rates,
        integrates the rates in a sliding window to calculate qumulative quantity,
        saves the results to Cassandra """

    # Kafka and Spark Streaming specific vars
    batchLength = 60
    window_length = 60

    sc = SparkContext(appName="streamingIoTData")
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sc, batchLength)
    ssc.checkpoint("hdfs://master.rquitales.com:9000/usr/sp_data")

    zkQuorum, topic1, topic2 = 'localhost:2181', 'radiation', 'air-quality'
    # Specify all the nodes you are running Kafka on
    kafkaBrokers = {"metadata.broker.list": "localhost:9092"}

    # Get the sensor and location data streams - they have separate Kafka topics
    radiationData = KafkaUtils.createDirectStream(ssc, [topic1], kafkaBrokers)
    airData = KafkaUtils.createDirectStream(ssc, [topic1], kafkaBrokers)

    ##### Merge streams and push rates to Cassandra #####

    # Get location (room) info for users
    rawRadiation = kafa2Json(radiationData).count().map(lambda x:'Radiations in this batch: %s' % x).pprint()
    rawAir = kafa2Json(airData).count().map(lambda x:'Airs in this batch: %s' % x).pprint

    #sRad = rawRadiation.map(lambda x: ((x["radiation"]["deviceID"], x["radiation"]["ctime"], x["radiation"]["latitude"], x["radiation"]["longitude"]) , x["radiation"]["value"]))
    #sAir = rawAir.map(lambda x: ((x["air-quality"]["deviceID"], x["air-quality"]["ctime"], x["air-quality"]["latitude"], x["air-quality"]["longitude"]), x["air-quality"]["value"]))

    #combinedInfo = sRad.join(sAir).persist(StorageLevel.MEMORY_ONLY)

    #combinedInfo.pprint()

    ssc.start()
    ssc.awaitTermination()

if __name__ == '__main__':
  main()



 combinedInfoAvg = combinedInfo.map(lambda x: (x[0][0], (x[0][1], x[0][2], x[0][3], x[1][0], x[1][1]))).groupByKey().\
        map(lambda x : (x[0][0], (x[0][1], x[0][0], (x[0][1], x[0][2], x[0][3], reduce(lambda x, y: x + y, list(x[1]))/float(len(list(x[1]))))))).persist(StorageLevel.MEMORY_ONLY)

    combinedInfoAvg.pprint()
