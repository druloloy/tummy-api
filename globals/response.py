from flask import jsonify, make_response

def basic_response(message: str, data: dict = None, status_code: int = 200):
    response = make_response(jsonify({"message": message, "data": [] if not data else data}), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response

def error_response(error_message: str, error, status_code: int = 500):
    response = make_response(jsonify({"error": error_message, "stack": str(error), "instance": error.__class__.__name__}), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response