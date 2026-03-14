import requests
from config import SERVER_URL
def send_chat_message(user_message,settings):
    """Sends a chat message to the backend API."""
    headers = {"Content-Type": "application/json"}
    from functions.preparePayload import prepare_payload
    payload = prepare_payload(user_message=user_message, settings=settings)
    response = requests.post(SERVER_URL, json=payload, headers=headers)
    print("API Response :", response.status_code, response.text)
    return response.json()