#!/bin/bash
numRecords=$(($1 + 1))

#Create file with specified number of lines as seed/bootstrap file.
head -n $numRecords japanSafecast.txt > unique$1.txt

python3 ./payloadGen.py $1 1 &
python3 ./payloadGen_air.py $1 1 &
wait &&
aws s3 cp payload_air.txt s3://iotdatas3/payload_air.txt &
aws s3 cp payload.txt s3://iotdatas3/payload.txt &
wait &&
echo "All done!"
