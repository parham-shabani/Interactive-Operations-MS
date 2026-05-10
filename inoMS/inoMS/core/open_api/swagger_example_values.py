bad_request_error = {
    "data": None,
    "message": None,
    "status_code": 400,
    "errors": {"name": "string"},
    "success": False,
}

unauthorized_error = {
    "data": None,
    "message": "Authentication credentials were not provided.",
    "status_code": 401,
    "errors": {},
    "success": False,
}

forbidden_access_error = {
    "data": None,
    "message": "Forbidden access",
    "status_code": 403,
    "errors": {},
    "success": False,
}

not_found_error = {
    "data": None,
    "message": "Not found.",
    "status_code": 404,
    "errors": {},
    "success": False,
}

too_many_requests_error = {
    "data": None,
    "message": "string",
    "status_code": 429,
    "errors": {},
    "success": False,
}

internal_server_error = {
    "data": None,
    "message": "Internal server error",
    "status_code": 500,
    "errors": {},
    "success": False,
}
