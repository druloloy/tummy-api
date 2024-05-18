from apps.ai.configs.gemini import get_model

def generate_autocomplete_ingredients(query):
    model = get_model('tunedModels/ingredients-api-model-tuned-kcneo0ob5lgn')
    prompt_parts = [
        "Generate up to 8 suggestions for food ingredients based on a given query. Each suggestion should include the ingredient name and its processing type, if applicable.\nFood ingredients include pork, fish, beef, and other meat products.\nResponse should be structured like a JS Array.Example:[\"Banana\",\"Banana, sliced\",\"Banana chips\",\"Banana bread\",\"Banana muffins\",\"Banana smoothie\",\"Banana pudding\",\"Plantain\"]\nInstructions:1. Provide a query string, such as \"Oni\".2. Generate up to 8 suggestions for food ingredients based on the provided query.3. Ensure that each suggestion includes the ingredient name and its processing type, if applicable (e.g., \"Onion, chopped\").",
        "input: " + query,
        "output: "
    ]

    return model.generate_content(prompt_parts).text
