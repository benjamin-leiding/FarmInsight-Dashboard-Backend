from rest_framework import views, status
from rest_framework.response import Response
from farminsight_dashboard_backend.services import store_measurements_in_influx

class MeasurementView(views.APIView):
    def post(self, request, sensor_id):
        """
        Store a single or a set of measurements for a given sensor in the InfluxDB
        at the fpf bucket
        :param request: HTTP request
        :param sensor_id: GUID of the sensor
        :return: HTTP response
        """
        store_measurements_in_influx(sensor_id, request.data)
        return Response({"message": "Data written successfully"}, status=status.HTTP_201_CREATED)
