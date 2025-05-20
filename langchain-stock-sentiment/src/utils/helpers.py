def format_json_response(data):
    return {
        "status": "success",
        "data": data
    }

def handle_api_error(error_message):
    return {
        "status": "error",
        "message": error_message
    }