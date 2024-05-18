def register_routes(blueprint):
    from apps.user.routes import register_user_route
    register_user_route(blueprint)

    from apps.recipe.routes import register_recipe_route
    register_recipe_route(blueprint)

    from apps.ai.routes import register_ai_route
    register_ai_route(blueprint)