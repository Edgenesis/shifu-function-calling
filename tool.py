# a python function that gets localhost:3001/capture and returns the captured image
# the /capture endpoint returns a png image data

import requests
import base64
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def get_image() -> bytes:
    response = requests.get("http://localhost:3001/capture")
    return response.content


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_image",
            "description": "A function that gets an image from the /capture endpoint.",
        },
    }
]

prompt = [
    {
        "role": "system",
        "content": "You are a helpful surveillance assistant. Use the supplied tools to assist the user.",
    },
    {"role": "user", "content": "Hi, can you tell what the camera is seeing?"},
]


def handle_function_call(tool_call):
    if tool_call.function.name == "get_image":
        image = get_image()
        with open("image.png", "wb") as f:
            f.write(image)
        return base64.b64encode(image).decode('utf-8')


def test_completion():
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini", messages=prompt, tools=tools
    )
    tool_call = chat_completion.choices[0].message.tool_calls[0]
    print(tool_call)
    function_call_output = handle_function_call(tool_call)
    prompt.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Thanks! Can you tell me what is in the image?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{function_call_output}",
                    },
                },
            ],
        }
    )
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini", messages=prompt, tools=tools
    )
    print(chat_completion.choices[0].message.content)


test_completion()
