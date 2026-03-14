import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
from config import MODELS
async def chat_settings():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Select model used for chat completion",
                values=MODELS,
                initial_index=0,
            ),
            Switch(id="Streaming", label="Stream Tokens", initial=True),
            Slider(
                id="Temperature",
                label="Temperature",
                initial=0.5,
                min=0,
                max=2,
                step=0.1,
            )
        ]
    ).send()
    return settings

