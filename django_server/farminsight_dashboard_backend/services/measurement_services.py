from farminsight_dashboard_backend.models import Sensor
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from django.conf import settings


def store_measurements_in_influx(sensor_id, data):
    sensor = Sensor.objects.get(id=sensor_id)

    influxdb_settings = getattr(settings, 'INFLUXDB_CLIENT_SETTINGS', {})

    client = InfluxDBClient(url=influxdb_settings['url'],
                            token=influxdb_settings['token'],
                            org=influxdb_settings['org'])

    write_api = client.write_api(write_options=SYNCHRONOUS)

    points = []
    for measurement in data:
        point = (
            Point("SensorData")
            .tag("sensorId", str(sensor_id))
            .field("value", float(measurement['value']))
            .time(measurement['measuredAt'], WritePrecision.NS)
        )
        points.append(point)

    write_api.write(bucket=str(sensor.FPF_id), record=points)
    client.close()