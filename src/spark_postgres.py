"""
/usr/local/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 ~/insightProject/src/sparkStreaming.py
/usr/local/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0,org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 ~/insightProject/src/sparkStreaming.py
"""

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import sys, json, psycopg2, os
from datetime import datetime
from pyspark import StorageLevel
from pyspark.sql.functions import sum
from pyspark.sql.types import *
from pyspark.sql import Window
from pyspark.sql import SQLContext
from pyspark.sql import functions
from pyspark.streaming.util import rddToFileName, TransformFunction

#Modified foreachRDD function to increase throughput connection with Postgres
def foreachRDD_modified(self, func):
        """
        Apply a function to each RDD in this DStream.
        """
        if func.__code__.co_argcount == 1:
            old_func = func
            func = lambda t, rdd: old_func(rdd)
        jfunc = TransformFunction(self._sc, func, self._jrdd_deserializer)
        api = self._ssc._jvm.PythonDStream
        print("")
        print("############################################################")
        print("#                                                          #")
        print("#                  Opening DB Connection                   #")
        print("#                                                          #")
        print("############################################################")
        print("Spark Processing Starting: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print("")
        print("------------------------------------------------------------")
        print("")
        #Create DB connection here as Spark's lazy evaluation will only create the DB connection once at the start of job
        global conn
        conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s"%(os.environ['psqlDB'], os.environ['psqlUser'], os.environ['psqlPwd'], os.environ['psql']))
        global cur
        cur = conn.cursor()
        api.callForeachRDD(self._jdstream, jfunc)

#Actual INSERT query function
def save2postgres(time, rdd):
  if not rdd.isEmpty():
    taken = rdd.take(sys.maxsize)
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " - Number of records sent to DB: " + str(len(taken)))
    for data in taken:
      cur.execute('INSERT INTO results VALUES (%s, %s, %s, %s, %s, %s)', (data['deviceid'], data['latitude'], data['longitude'], data['ctime'], data['radiation'], data['air']))
    conn.commit()

#Parse kafka output to json format
def kafa2Json(sensorData):
  """ Parse input json stream """
  rawSensor = sensorData.map(lambda k: json.loads(k[1]))
  return rawSensor

def main():
    # Kafka and Spark Streaming specific vars
    batchLength = 60

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

    ##### Merge streams and push rates to Postgres #####

    # Parse Kafka output
    rawRadiation = kafa2Json(radiationData)
    rawAir = kafa2Json(airData)

    sRad = rawRadiation.map(lambda x: ((x["radiation"]["deviceID"], datetime.strptime(x["radiation"]["ctime"], "%Y-%m-%d %H:%M:%S"), x["radiation"]["latitude"], x["radiation"]["longitude"]) , x["radiation"]["value"]))
    sAir = rawAir.map(lambda x: ((x["airquality"]["deviceID"], datetime.strptime(x["airquality"]["ctime"], "%Y-%m-%d %H:%M:%S"), x["airquality"]["latitude"], x["airquality"]["longitude"]), x["airquality"]["value"]))

    #Get averages of both streams and calibrate data.
    radAvg = sRad.map(lambda x: ((x[0][0], x[0][2], x[0][3]), x[1])).\
                     mapValues(lambda v: (v, 1)).\
                     reduceByKey(lambda a,b: (a[0]+b[0], a[1]+b[1]))
    radResult = radAvg.mapValues(lambda v: v[0]/v[1])
    radResult = radResult.map(lambda x: ((x[0][0], x[0][1], x[0][2], datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 0.002956*x[1]-0.010132))

    airAvg = sAir.map(lambda x: ((x[0][0], x[0][2], x[0][3]), x[1])).\
                     mapValues(lambda v: (v, 1)).\
                     reduceByKey(lambda a,b: (a[0]+b[0], a[1]+b[1]))
    airResult = airAvg.mapValues(lambda v: v[0]/v[1])
    airResult = airResult.map(lambda x: ((x[0][0], x[0][1], x[0][2], datetime.now().strftime('%Y-%m-%d %H:%M:%S')), x[1]))

    #Merge streams
    finalResult = radResult.join(airResult).persist(StorageLevel.MEMORY_ONLY)
    finalResult = finalResult.map(lambda x: {"deviceid": x[0][0], "latitude": x[0][1], "longitude": x[0][2], "ctime": x[0][3], "radiation": x[1][0], "air": x[1][1]})

    #Save to Postgres, with higher efficiency. Function call now, not class attribute
    foreachRDD_modified(finalResult, save2postgres)

    ssc.start()
    ssc.awaitTermination()
    cur.close()
    conn.close()
    print("All DB connections closed.")

if __name__ == '__main__':
  main()
