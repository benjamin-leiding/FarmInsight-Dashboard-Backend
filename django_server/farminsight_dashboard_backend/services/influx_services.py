from influxdb_client import InfluxDBClient, Point, WritePrecision
from django.conf import settings
from influxdb_client.client.write_api import SYNCHRONOUS

from farminsight_dashboard_backend.exceptions import InfluxDBQueryException, InfluxDBNoConnectionException
from farminsight_dashboard_backend.models import FPF
import requests
import logging
import threading


class InfluxDBManager:
    """
    InfluxDBManager to manage all interactions with the influx database, implemented as a Singleton.
    """
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def __new__(cls, *args, **kwargs):
        return super(InfluxDBManager, cls).__new__(cls)

    def __init__(self):
        """
        Initialize the InfluxDB manager with settings and a logger.
        """
        if not getattr(self, "_initialized", False):
            self.influxdb_settings = getattr(settings, 'INFLUXDB_CLIENT_SETTINGS', {})
            self.client = None
            self.log = logging.getLogger("farminsight_dashboard_backend")
            self._initialized = True

    def initialize_connection(self):
        """
        Attempt to connect to InfluxDB and synchronize FPF buckets.
        """
        if not self.influxdb_settings:
            self.log.warning("InfluxDB settings not found. Skipping InfluxDB setup.")
            return

        try:
            self.client = InfluxDBClient(
                url=self.influxdb_settings['url'],
                token=self.influxdb_settings['token'],
                org=self.influxdb_settings['org']
            )

            if not self.client.ping():
                raise ConnectionError("InfluxDB is not reachable.")

            self.sync_fpf_buckets()
            self.log.info("InfluxDB database connection successful.")

        except (requests.exceptions.RequestException, ConnectionError) as e:
            self.log.warning(f"InfluxDB connection failed: {e} Proceeding without InfluxDB.")
            self.client = None

    def sync_fpf_buckets(self):
        """
        Ensure each FPF in SQLite has a corresponding bucket in InfluxDB.
        """
        try:
            if not self.client:
                self.log.warning("InfluxDB client is not initialized.")
                return

            bucket_api = self.client.buckets_api()
            fpf_objects = FPF.objects.all()

            if not fpf_objects.exists():
                self.log.warning("No FPFs found in the database.")
                return

            for fpf in fpf_objects:
                bucket_name = str(fpf.id)
                if not bucket_api.find_bucket_by_name(bucket_name):
                    self.log.info(f"Creating new bucket: {bucket_name}")
                    bucket_api.create_bucket(bucket_name=bucket_name, org=self.influxdb_settings['org'])

        except Exception as e:
            self.log.error(f"Failed to sync FPF buckets with InfluxDB: {e}")

    def fetch_sensor_measurements(self, fpf_id: str, sensor_ids: list, from_date: str, to_date: str) -> dict:
        """
        Queries InfluxDB for measurements within the given date range for multiple sensors.
        :param fpf_id: The ID of the FPF (used as the bucket name in InfluxDB).
        :param sensor_ids: List of sensor IDs to query data for.
        :param from_date: Start date in ISO 8601 format.
        :param to_date: End date in ISO 8601 format.
        :return: Dictionary with sensor IDs as keys, each containing a list of measurements.
        """

        if not self.client:
            self.log.error("InfluxDB client is not initialized.")
            raise InfluxDBNoConnectionException("InfluxDB client is not initialized.")

        try:
            query_api = self.client.query_api()

            # Build the filter part of the query for multiple sensors
            sensor_filter = " or ".join([f'r["sensorId"] == "{sensor_id}"' for sensor_id in sensor_ids])

            query = (
                f'from(bucket: "{fpf_id}") '
                f'|> range(start: {from_date}, stop: {to_date}) '
                f'|> filter(fn: (r) => r["_measurement"] == "SensorData" and ({sensor_filter}))'
            )

            result = query_api.query(org=self.influxdb_settings['org'], query=query)

            # Process and organize results by sensor ID
            measurements = {sensor_id: [] for sensor_id in sensor_ids}
            for table in result:
                for record in table.records:
                    sensor_id = record.values["sensorId"]
                    measurements[sensor_id].append({
                        "measuredAt": record.get_time().isoformat(),
                        "value": record.get_value()
                    })

        except requests.exceptions.ConnectionError as e:
            self.log.error(f"Failed to connect to InfluxDB: {e}")
            raise InfluxDBNoConnectionException("Unable to connect to InfluxDB.")

        except Exception as e:
            self.log.error(f"Failed to fetch sensor measurements from InfluxDB: {e}")
            raise InfluxDBQueryException(str(e))

        return measurements

    def write_sensor_measurements(self, fpf_id: str, sensor_id: str, measurements):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        points = []
        for measurement in measurements:
            point = (
                Point("SensorData")
                .tag("sensorId", str(sensor_id))
                .field("value", float(measurement['value']))
                .time(measurement['measuredAt'], WritePrecision.NS)
            )
            points.append(point)

        write_api.write(bucket=fpf_id, record=points)

    def close(self):
        """Close the InfluxDB client if it's open."""
        if self.client:
            self.client.close()
