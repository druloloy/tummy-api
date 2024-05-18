from flask import request, g
from globals.error.error_handler import handle_errors
from globals.error.exception import TummyError
from globals.response import basic_response
from apps.recipe.model import Recipe
from apps.user.model import User
from app import db
from firebase.auth import firebase_auth

PAGINATION_LIMIT = 10

def register_recipe_route(app):
    """
    Register recipe route with POST, PUT, and GET methods to create, update, and fetch recipe information.
    """
    @app.route('/recipe', methods=['POST'])
    @firebase_auth
    def create_recipe(fb_user):
        """
        Create a new recipe with the given data.
        Returns a JSON response with the recipe information and a 201 status code.
        """
        try:
            data = request.get_json()
            owner_id = fb_user.custom_claims['dbid']

            recipe = Recipe(
                _id=data.get('_id'),
                owner_id=owner_id,
                title=data.get('title'),
                description=data.get('description'),
                ingredients=data.get('ingredients'),
                procedure=data.get('procedure'),
                image_url=data.get('image_url')
            )

            db.session.add(recipe)
            db.session.commit()

            return basic_response(
                message="Recipe created successfully!",
                data=recipe.as_dict(),
            )

        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)

    @app.route('/recipe/user', methods=['GET'])
    def get_user_recipe():
        """
        Get all recipes.
        Returns a JSON response with a list of recipe information and a 200 status code.
        """
        try:
            # TODO: Get user id from claims
            id = request.args.get('_id')
            offset = int(request.args.get('offset')) if request.args.get('offset') else 0

            user: User = User.query.filter_by(_id=id).first()
            
            if not user:
                raise TummyError('User not found!', 400)

            recipes = list(user.recipes)[offset:offset+PAGINATION_LIMIT]

            if not recipes and len(user.recipes) == 0:
                raise TummyError('No recipes found!', 400)

            return basic_response(
                message="Recipes fetched successfully!",
                data={
                    'recipes': [recipe.as_dict() for recipe in recipes],
                    'owner': user.as_discreet_dict('email', '_auth_id'),
                    'returned_size': len(recipes),
                    'total_results': len(user.recipes),
                    'offset': offset,
                    'limit': PAGINATION_LIMIT
                }
            )

        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)
    
    @app.route('/recipe/anon', methods=['GET'])
    def get_all_recipe_anon():
        """
        Get all recipes.
        Returns a JSON response with a list of recipe information and a 200 status code.
        """
        try:
            id = request.args.get('_id')
            offset = int(request.args.get('offset')) if request.args.get('offset') else 0

            user: User = User.query.filter_by(_id=id).first()

            if not user:
                raise TummyError('User not found!', 400)

            recipes = list(user.recipes)[offset:offset+PAGINATION_LIMIT]

            if not recipes and len(user.recipes) == 0:
                raise TummyError('No recipes found!', 400)

            return basic_response(
                message="Recipes fetched successfully!",
                data={
                    'recipes': [recipe.as_dict() for recipe in recipes],
                    'owner': user.as_discreet_dict('email', '_auth_id'),
                    'returned_size': len(recipes),
                    'total_results': len(user.recipes),
                    'offset': offset,
                    'limit': PAGINATION_LIMIT
                }
            )

        
        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)
    
    @app.route('/recipe', methods=['GET'])
    def get_single_recipe():
        """
        Get a single recipe by ID.
        Returns a JSON response with the recipe information and a 200 status code if the recipe was found.
        """
        try:
            id = request.args.get('_id')
            recipe = Recipe.query.filter_by(_id=id).first()

            if not recipe:
                raise TummyError('Recipe not found!', 400)

            return basic_response(
                message="Recipe fetched successfully!",
                data=recipe.as_dict(),
            )
        
        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)
