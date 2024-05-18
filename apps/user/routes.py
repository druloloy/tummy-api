from flask import request, make_response, jsonify, g
from apps.user.model import User
from app import db
from psycopg2.errorcodes import UNIQUE_VIOLATION
from sqlalchemy.exc import OperationalError, IntegrityError
from globals.error.error_handler import handle_errors
from globals.error.exception import TummyError
from globals.response import basic_response
from firebase.auth import firebase_auth, auth

def register_user_route(app):
    """
    Register user route with POST, PUT, and GET methods to create, update, and fetch user information.
    """

    @app.route('/user', methods=['POST'])
    def create_user():
        """
        Create a new user with the given data.
        Returns a JSON response with the user information and a 201 status code.
        """
        try:
            data = request.get_json()
            
            user = User(
                _auth_id=data.get('_auth_id'),
                email=data.get('email'),
                username=data.get('username'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                dob=data.get('dob'),
                gender=data.get('gender')
            )

            db.session.add(user)
            db.session.commit()

            _id = user.__getattribute__('_id')

            auth.set_custom_user_claims(data.get('_auth_id'), {
                "dbid": str(_id),
                "email": data.get('email'),
                "username": data.get('username')
            })

            return basic_response(
                message="User created successfully!",
                data=user.as_dict(),
                status_code=201
            )

        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)
        finally:
            db.session.close()

    @app.route('/user', methods=['PUT'])
    @firebase_auth
    def update_user(fb_user):
        """
        Update an existing user with the given data.
        Returns a JSON response with a 200 status code if the user was updated successfully.
        """
        try:
            data = request.get_json()
            id = request.args.get('_id')
            # return keys and values to be updated if value is not empty, undefined or null
            update_fields = {key: value for key, value in data.items()
                             if value is not None and key not in ('_id', '_auth_id', 'email', 'username')}

            if not update_fields:
                raise TummyError("No fields to update", 400)

            User.query.filter_by(_id=id).update(update_fields)

            db.session.commit()

            return basic_response(
                message="User updated successfully!",
                status_code=200
            )

        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)
        finally:
            db.session.close()

    @app.route('/user', methods=['GET'])
    def get_user():
        """
        Retrieve the currnet user.
        Returns a JSON response with the user information and a 200 status code if the user was found.
        """
        try:
            # TODO: Get user id from claims
            id = request.args.get('_id')

            if not id: 
                raise TummyError('User is not logged in!', 401)

            user = User.query.filter_by(_id=id).first()

            return basic_response(
                message="User fetched successfully!",
                data=user.as_dict(),
                status_code=200
            )

        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)
        finally:
            db.session.close()

    @app.route('/user/anon', methods=['GET'])
    def get_anon_user():
        """
        Retrieve a user by their ID.
        Returns a JSON response with the user information and a 200 status code if the user was found.
        """
        try:
            id = request.args.get('_id')
            user = User.query.filter_by(_id=id).first()

            if not user:
                raise TummyError('User not found!', 400)

            return basic_response(
                message="User fetched successfully!",
                data=user.as_discreet_dict('email', '_auth_id'),
                status_code=200
            )

        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)
        finally:
            db.session.close()
    
    @app.route('/user/availability', methods=['GET'])
    def check_user_availability():
        """
        Check if a user with the given email or username exists.
        """
        try:
            email = request.args.get('email')
            username = request.args.get('username')
            user = User.query.filter(
                (User.username==username) | (User.email==email)
            ).first()

            if user:
                raise TummyError('Username or email already exists.', 400)

            return basic_response(
                message="Username or email is available."
            )

        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)
        finally:
            db.session.close()