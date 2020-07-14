"""rest-framework exception handler"""

import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import exception_handler
from .result_handler import (ResultGenerator, NOT_FOUND, UNAUTHORIZED, FORBIDDEN)
from .exceptions import ServiceError

logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        status_code = response.status_code
        if status_code == 404:
            return ResultGenerator.gen_result(NOT_FOUND)
        elif status_code == 401:
            return ResultGenerator.gen_result(UNAUTHORIZED)
        elif status_code == 403:
            logger.warning(exc)
            msg = exc.default_code
            return ResultGenerator.gen_result(FORBIDDEN, msg)
        elif status_code == 400:
            logger.warning(exc)
            return ResultGenerator.gen_fail_result('bad request')
        elif status_code == 500:
            return ResultGenerator.gen_error_result()
        msg = exc.default_code
        return ResultGenerator.gen_fail_result(msg)
    elif exc is not None:
        if isinstance(exc, ObjectDoesNotExist):
            return ResultGenerator.gen_no_content_result()
        elif isinstance(exc, ServiceError):
            msg = exc.message
            logger.info(msg)
            return ResultGenerator.gen_fail_result(msg)
        elif isinstance(exc, Exception):
            logger.exception(exc)
            return ResultGenerator.gen_error_result()

    return response
