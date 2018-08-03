#!/bin/bash

python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 1 'radiation' 10 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 1 'airquality' 10 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 11 'radiation' 10 11 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 11 'airquality' 10 11 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 22 'radiation' 10 22 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 22 'airquality' 10 22 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 33 'radiation' 10 33 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 33 'airquality' 10 33 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 44 'radiation' 10 44 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 44 'airquality' 10 44 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 55 'radiation' 10 55 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 55 'airquality' 10 55 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 66 'radiation' 10 66 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 66 'airquality' 10 66 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 77 'radiation' 10 77 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 77 'airquality' 10 77 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 88 'radiation' 10 88 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 88 'airquality' 10 88 &
python3 ./streamData.py 'radiation' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 99 'radiation' 10 499 &
python3 ./streamData.py 'airquality' '../input/ipAddresses.txt' '../input/japanSafecast.txt' 99 'airquality' 10 99 &
wait
echo 'All done!'
