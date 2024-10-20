

## Set up InfluxDB in Docker

Set up local environment file
/django-server/.env.dev example:
```
INFLUXDB_URL=http://localhost:8086
DOCKER_INFLUXDB_INIT_USERNAME=admin
INFLUXDB_INIT_PASSWORD=your_password
INFLUXDB_INIT_TOKEN=your_token
DOCKER_INFLUXDB_INIT_ORG=ETCE-LAB
```

Install Docker.

Create/Run the influx db docker container manually (don't do this, it's only for reference):
```
# Pull the latest InfluxDB Docker image
docker pull influxdb:latest

# Run the InfluxDB container
docker run -d --name influxdb -p 8086:8086 -v influxdb-storage:/var/lib/influxdb2 influxdb:latest
```
With docker-compose (do this):

* To start
```
docker-compose --env-file .env.dev up -d
```
* To stop
```
docker-compose down 
```

On server start, it will automatically add a bucket per fpf in the InfluxDB.

Example data check in the Influx cli:
```
influx query 'from(bucket:"c7e6528b-76fd-4895-8bb9-c6cd500fc152") |> range(start: -1000y) |> filter(fn: (r) => r._measurement == "SensorData")'
```