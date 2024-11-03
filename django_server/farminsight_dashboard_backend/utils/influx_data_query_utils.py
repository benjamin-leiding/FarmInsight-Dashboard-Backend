from influxdb_client import InfluxDBClient
from django.conf import settings


def fetch_sensor_measurements(fpf_id: str, sensor_ids: list, from_date: str, to_date: str) -> dict:
    """
    Queries InfluxDB for measurements within the given date range for multiple sensors.

    :param fpf_id: The ID of the FPF (used as the bucket name in InfluxDB).
    :param sensor_ids: List of sensor IDs to query data for.
    :param from_date: Start date in ISO 8601 format.
    :param to_date: End date in ISO 8601 format.
    :return: Dictionary with sensor IDs as keys, each containing a list of measurements.
    """

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

    max_points = int(getattr(settings, 'MAX_MEASUREMENTS_PER_REQUEST', {}))
    # Check the number of data points and aggregate if necessary
    for sensor_id, data_points in measurements.items():
        if len(data_points) > max_points:
            measurements[sensor_id] = aggregate_data(data_points, max_points)

    return measurements


def aggregate_data(data_points, max_points):
    """
    Aggregate data points by calculating the mean for segments to reduce the total number.
    """
    # Calculate the number of data points per segment
    segment_size = max(1, len(data_points) // max_points)
    aggregated_data = []

    for i in range(0, len(data_points), segment_size):
        segment = data_points[i:i + segment_size]

        # Calculate the mean of the segment
        mean_value = sum(point["value"] for point in segment) / len(segment)
        mean_timestamp = segment[len(segment) // 2]["measuredAt"]

        aggregated_data.append({
            "measuredAt": mean_timestamp,
            "value": mean_value
        })

    return aggregated_data
