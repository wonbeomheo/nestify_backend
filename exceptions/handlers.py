from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging
import os

logger = logging.getLogger(os.environ.get('DJANGO_DEBUG'))

def nestify_exception_handler(exc, context):
  logger.error(exc)
  # if APIException
  response = Response(
    data=exc.get_full_details()
  )
  # if SystemError
  
  return response