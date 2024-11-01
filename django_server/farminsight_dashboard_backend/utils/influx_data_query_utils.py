from influxdb_client import InfluxDBClient
from django.conf import settings

def fetch_sensor_measurements(fpf_id, sensor_ids, from_date, to_date):
    """
    Queries InfluxDB for measurements within the given date range for multiple sensors.

    :param fpf_id: The ID of the FPF (used as the bucket name in InfluxDB).
    :param sensor_ids: List of sensor IDs to query data for.
    :param from_date: Start date in ISO 8601 format.
    :param to_date: End date in ISO 8601 format.
    :return: Dictionary with sensor IDs as keys, each containing a list of measurements.
    """
    print(fpf_id, sensor_ids, from_date, to_date)

    influxdb_settings = getattr(settings, 'INFLUXDB_CLIENT_SETTINGS', {})
    client = InfluxDBClient(
        url=influxdb_settings['url'],
        token=influxdb_settings['token'],
        org=influxdb_settings['org']
    )
    query_api = client.query_api()

    # Build the filter part of the query for multiple sensors
    sensor_filter = " or ".join([f'r["sensorId"] == "{sensor_id}"' for sensor_id in sensor_ids])

    query = (
        f'from(bucket: "{fpf_id}") '
        f'|> range(start: {from_date}, stop: {to_date}) '
        f'|> filter(fn: (r) => r["_measurement"] == "SensorData" and ({sensor_filter}))'
    )

    result = query_api.query(org=influxdb_settings['org'], query=query)
    client.close()

    # Process and organize results by sensor ID
    measurements = {sensor_id: [] for sensor_id in sensor_ids}
    for table in result:
        for record in table.records:
            sensor_id = record.values["sensorId"]
            measurements[sensor_id].append({
                "measuredAt": record.get_time().isoformat(),
                "value": record.get_value()
            })

    return measurements