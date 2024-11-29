from django.apps import AppConfig
import os
import threading


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
            from farminsight_dashboard_backend.services import InfluxDBManager, start_scheduler
            threading.Thread(target=InfluxDBManager.get_instance().initialize_connection, daemon=True).start()
            threading.Thread(target=start_scheduler, daemon=True).start()
