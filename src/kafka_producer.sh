#!/bin/bash

#Use kafka's own utility to send payload files at specified rates.
/usr/local/kafka/bin/kafka-producer-perf-test.sh --topic radiation --num-records 2400000 --payload-file '/home/ubuntu/payload_sm.txt' --throughput 10000 --producer-props bootstrap.servers=localhost:9092 &
/usr/local/kafka/bin/kafka-producer-perf-test.sh --topic airquality --num-records 2400000 --payload-file '/home/ubuntu/payload_air_sm.txt' --throughput 10000 --producer-props bootstrap.servers=localhost:9092 &
wait &&
echo "All done!"
