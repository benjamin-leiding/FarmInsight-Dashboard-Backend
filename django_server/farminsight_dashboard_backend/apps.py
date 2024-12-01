from django.apps import AppConfig
import os
import threading

from django.db.models.signals import post_migrate


class FarminsightDashboardBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'farminsight_dashboard_backend'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ready(self):
        """
        Start a new thread to check for pending migrations and start the scheduler if ready
        """

        if os.environ.get('RUN_MAIN') == 'true':
            from farminsight_dashboard_backend.services import InfluxDBManager, CameraScheduler
            from django.db import connections

            def initialize_services(sender, **kwargs):
                if connections['default'].is_usable():
                    threading.Thread(
                        target=InfluxDBManager.get_instance().initialize_connection, daemon=True
                    ).start()
                    threading.Thread(
                        target=CameraScheduler.get_instance().start, daemon=True
                    ).start()

            post_migrate.connect(initialize_services, sender=self)
