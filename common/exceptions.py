from rest_framework.views import exception_handler
from rest_framework.serializers import ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from django.http import HttpResponse, JsonResponse


def flatten_error(detail):
    if isinstance(detail, (list, ReturnList)):
        return [flatten_error(item) for item in detail]
    elif isinstance(detail, (dict, ReturnDict)):
        return {key: flatten_error(value) for key, value in detail.items()}
    elif isinstance(detail, ErrorDetail):
        return str(detail)
    return detail


def get_error_message(detail):
    if isinstance(detail, dict):
        first_key = next(iter(detail))
        first_error = detail[first_key]
        if isinstance(first_error, (list, ReturnList)):
            return str(first_error[0])
        return str(first_error)
    elif isinstance(detail, (list, ReturnList)):
        return str(detail[0])
    return str(detail)


def custom_exception_handler(exc, context):
    """
    Handles both DRF exceptions and HTML errors.
    Returns all responses in the unified APIResponse structure.
    """
    # Try DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Standard DRF exception
        error_detail = flatten_error(response.data)
        message = get_error_message(error_detail)
        response.data = {
            "success": False,
            "data": None,
            "error": error_detail,
            "message": message
        }
        return response

    # If response is None, it might be an HTML error (e.g., 404 or 500)
    # Fallback: wrap in JSON
    # Try to get status code from exception, default to 500
    status_code = getattr(exc, "status_code", 500)
    return JsonResponse(
        {
            "success": False,
            "data": None,
            "error": {"detail": str(exc)},
            "message": "Request failed"
        },
        status=status_code
    )
