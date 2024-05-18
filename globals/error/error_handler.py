from flask import jsonify
from globals.error.exception import TummyError
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from app import db
from firebase_admin.auth import InvalidIdTokenError
from globals.response import error_response

def handle_errors(e):
    if isinstance(e, TummyError):
        return error_response(e.error, e, e.status_code)
    if isinstance(e, AssertionError):
        return error_response(e.args[0], e, 400)
    if isinstance(e, IntegrityError):
        db.session.rollback()
        return error_response("Something went wrong and we are fixing it.", e, 400)
    if isinstance(e, InvalidIdTokenError):
        return error_response("Invalid token provided.", e, 401)
    if isinstance(e, DataError):
        db.session.rollback()
        return error_response("Input data is malformed or invalid type.", e, 400)    
    if isinstance(e, OperationalError):
        db.session.rollback()
        return error_response("Something went wrong and we are fixing it.", e, 500)
    
    return error_response("Something went wrong and we are fixing it.", e, 500)