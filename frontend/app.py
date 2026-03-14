import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import chainlit as cl
from functions.sendingChat import send_chat_message
from functions.displayResources import get_resource_usage
from chainlit.input_widget import Select, Switch, Slider
from config import MODELS
from typing import Optional
@cl.oauth_callback
def oauth_callback(provider_id: str, token: str, raw_user_data: dict, default_user: cl.User) -> Optional[cl.User]:
    default_user.metadata = {
            "user_data_prompt": {
                "role": "user",
                "content": f"This is user {raw_user_data.get('name')} with email {raw_user_data.get('email')}"
            }
        }
    return default_user
@cl.on_chat_start
async def start():
    app_user = cl.user_session.get("user")
    await cl.Message(
        content=f"Hello {app_user.identifier}! You have successfully logged in."
    ).send()
    user_data_prompt = app_user.metadata.get("user_data_prompt")
    cl.user_session.set("user_data", user_data_prompt)    
    settings = await cl.ChatSettings(
        [
            Select(id="Model",label="Select model used for chat completion", values=MODELS, initial_index=0 ),
            Switch(id="Streaming", label="Stream Tokens", initial=True),
            Slider(id="Temperature", label="Temperature", initial=0.5, min=0, max=2, step=0.1)
        ]
    ).send()
    cl.user_session.set("settings", settings)
@cl.on_settings_update
async def setup_agent(settings):
    cl.user_session.set("settings", settings)
@cl.on_message
async def main(message: cl.Message):
    settings = cl.user_session.get("settings")
    conversation = cl.chat_context.to_openai()
    prompt = cl.user_session.get("user_data_prompt")
    print("User Data Prompt :", prompt)
    print("Conversation History :", conversation)
    response = send_chat_message(conversation,settings)
    usage_data = await get_resource_usage(response=response) 
    usage_element = cl.CustomElement(
        name="ResourceUsage", 
        props=usage_data
    )
    cl.user_session.set("resource_usage", usage_element)
    print(response)
    await cl.Message(
        content=f" {response['choices'][0]['message']['content']}",
        elements=[usage_element]
    ).send()