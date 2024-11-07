from django.apps import AppConfig
from django.db.utils import OperationalError
from influxdb_client import InfluxDBClient
from django.conf import settings
import logging
import requests
import os
import threading

logger = logging.getLogger(__name__)


class FarminsightDashboardBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'farminsight_dashboard_backend'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(__name__)

    def ready(self):
        """
        Start a new thread to check for pending migrations and start the scheduler if ready
        """
        if os.environ.get('RUN_MAIN') == 'true':
            threading.Thread(target=self.setup_influxdb, daemon=True).start()

    def setup_influxdb(self):
        """
        Try to connect to the influxDB
        """
        try:
            from .models import FPF

            client = None
            influxdb_settings = getattr(settings, 'INFLUXDB_CLIENT_SETTINGS', {})

            if not influxdb_settings:
                self.log.warning("InfluxDB settings not found. Skipping InfluxDB setup.")
                return

            try:
                client = InfluxDBClient(url=influxdb_settings['url'],
                                        token=influxdb_settings['token'],
                                        org=influxdb_settings['org'])

                bucket_api = client.buckets_api()

                if not client.ping():
                    raise ConnectionError("InfluxDB is not healthy or reachable.")

                if not FPF.objects.exists():
                    self.log.warning("Unable to find any FPFs in the database.")
                    return

                for fpf in FPF.objects.all():
                    if not bucket_api.find_bucket_by_name(str(fpf.id)):
                        self.log.info(f"Creating new bucket: {fpf.id}")
                        bucket_api.create_bucket(bucket_name=str(fpf.id),
                                                 org=influxdb_settings['org'])

            except (requests.exceptions.RequestException, ConnectionError) as e:
                self.log.warning(f"InfluxDB connection failed: {e}. Proceeding without InfluxDB.")

            finally:
                client.close()

        except OperationalError:
            self.log.warning("Database not ready. Skipping InfluxDB setup.")
