"""
/usr/local/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 ~/insightProject/src/sparkStreaming.py

/usr/local/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0,org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 ~/insightProject/src/sparkStreaming.py
"""
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import sys, json

from pyspark import StorageLevel

from pyspark.sql.functions import sum
from pyspark.sql.types import *
from pyspark.sql import Window
from pyspark.sql import SQLContext
from pyspark.sql import functions

def kafa2Json(sensorData):
  """ Parse input json stream """
  rawSensor = sensorData.map(lambda k: json.loads(k[1]))
  return rawSensor

def main():
    batchLength = 20

    sc = SparkContext(appName="streamingIoTData")
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sc, batchLength)
    ssc.checkpoint("hdfs://mspark.rquitales.com:9000/usr/sp_data")

    zkQuorum, topic1, topic2 = 'mkafka.rquitales.com:2181', 'radiation', 'airquality'
    # Specify all the nodes you are running Kafka on
    kafkaBrokers = {"metadata.broker.list": "mkafka.rquitales.com:9092"}

    # Get the sensor and location data streams - they have separate Kafka topics
    radiationData = KafkaUtils.createDirectStream(ssc, [topic1], kafkaBrokers)
    airData = KafkaUtils.createDirectStream(ssc, [topic2], kafkaBrokers)

    ##### Merge streams and print results #####

    rawRadiation = kafa2Json(radiationData)
    rawAir = kafa2Json(airData)

    sRad = rawRadiation.map(lambda x: ((x["radiation"]["deviceID"], x["radiation"]["ctime"], x["radiation"]["latitude"], x["radiation"]["longitude"]) , x["radiation"]["value"]))
    sAir = rawAir.map(lambda x: ((x["airquality"]["deviceID"], x["airquality"]["ctime"], x["airquality"]["latitude"], x["airquality"]["longitude"]), x["airquality"]["value"]))

    combinedInfo = sRad.join(sAir).persist(StorageLevel.MEMORY_ONLY)

    combinedInfo.pprint()

    ssc.start()
    ssc.awaitTermination()

if __name__ == '__main__':
  main()
