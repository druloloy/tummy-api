from apps.ai.functions.autocomplete_ingredients import generate_autocomplete_ingredients
from flask import request, jsonify
from globals.error.error_handler import handle_errors
from globals.error.error_handler import TummyError
from globals.response import basic_response

def register_ai_route(app):
    @app.route('/ai/ingredients/autocomplete', methods=['GET'])
    def get_autocomplete_ingredients():
        try:
            query = request.args.get('query')
            result = generate_autocomplete_ingredients(query)
            
            json_result = jsonify(result)

            if(json_result):
                return basic_response(
                    message="Ingredients fetched successfully!",
                    data=json_result
                )
            else:
                raise TummyError('Ingredients not found!', 400)

        except Exception as e:
            print('Error:', str(e))
            return handle_errors(e)