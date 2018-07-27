# Citizenisation

## Importance
As the prices of electronical components and sensors get cheaper over time, more and more IoT devices are popping up. An effective way to generate data on mass with these cheap devices is to incorporate citizen science. Citizen science projects can generate large volumes of data that require processing, since the computing processors on board the IoT devices are usually weak and cheap.

## Project Idea
A publically available dataset obtained through citizen science is the Safecast dataset. Sparked from the Japan Fukushima incident, more and more devices are being connected to the Safecast network to detect radiation levels (mSv/h) globally. As expected, the mass of these devices are located within Fukushima and the wider Japan area. I intend on focussing on obtaining data within Japan and carry-out stream processing on the devices. As devices are cheap, the quality of instantaneous readings have large errors. The DE challenge for this would be to do a streaming rolling average of the last *x* timeframe constantly. Usually, most of these sensors are uncalibrated, so attaching a ML library (linear regression) for calibration could be done for a device per device case.

If time perimts, a batch process could also be done where daily/yearly trends are computed. A linear regression could also be computed (in place of a more advanced ML model) for forecasting.

## Relevant Technologies
  - S3/HDFS
    - Storage of data source for streaming simulation and for batch processing.
  - Kafka
    - Ingestion of streaming sensor data.
    - Ingestion of calibration parameters for linear modelling.
  - Spark Streaming
    - Processing of data. Averaging last *x* datapoints.
  - Spark ML
    - Calibration of device readings.
  - Spark - *extension*
    - Process older data for trends.
  - Cassandra (?.. or another GIS based database)
    - Storage of processed data.
  - Leaflet
    - Locality based visualisation.

### Proposed Pipeline
![Proposed pipeline.](./img/pipeline.jpg)

## DE Challenge(s)
  - Keeping track of data from specific devices within a timeframe (ie, averaging every 30 seconds of data per device). Rolling window aggregations.
  - Joining calibration parameters and device readings through device's ID.  -
  - Tracking location of device.
  - Averaging of calibrated readings within each device's vicinity.

## Data Source
Sample citizen science data from radiation sensors can be obtained from [Safecast](https://blog.safecast.org/data/). Uncompressed, the `.csv` file is ~12 GB in size. This will be used as the seed data to bootstrap the required amounts.
