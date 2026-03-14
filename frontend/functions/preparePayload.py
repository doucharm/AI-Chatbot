from config import DEFAULT_MODEL, DEFAUL_TEMPERATURE, DEFAULT_MAX_TOKENS
def prepare_payload(user_message,settings):
    if settings is None:
        settings = {
            "Model": DEFAULT_MODEL,
            "Temperature": DEFAUL_TEMPERATURE,
        }
    """Creates the JSON body for the API request."""
    return {
        "model": settings.get("Model", DEFAULT_MODEL),
        "messages": user_message,
        "temperature": settings.get("Temperature", DEFAUL_TEMPERATURE),
        "max_tokens": DEFAULT_MAX_TOKENS,   
    }
# This function can be expanded to include more parameters based on the settings available in the frontend.