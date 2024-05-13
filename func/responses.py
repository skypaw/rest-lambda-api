from json import dumps


def success_response(data):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": dumps(data),
    }


def bad_request_response(data):
    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": dumps(data),
    }


def not_found_response(data):
    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": dumps(data),
    }
