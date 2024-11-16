from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        logger.warning("A database integrity error occurred. " + str(exc))
        return Response(
            {"error": "A database integrity error occurred.", "details": str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, APIException):
        logger.warning(str(exc.default_detail) + str(exc.detail))
        return Response(
            {"error": exc.default_detail, "details": exc.detail},
            status=exc.status_code
        )

    if response is None:
        logger.warning("An unexpected error occurred." + str(exc))
        return Response(
            {"error": "An unexpected error occurred.", "details": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
