import streamlit as st
import openai
from openai import OpenAI
import json

password=st.text_input(label, type="password")
api_key = password
client = OpenAI(api_key=api_key)

def extract_question_information(function_answer):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "너는 사용자의 질문을 입력받아 응답을 하는 도우미야.",
            },
            {
                "role": "user",
                "content": function_answer,
            }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "extract_question_information",
                    "description": "사용자의 질문에 대답합니다.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "질문",
                            },
                            "arguments": {
                                "type": "string",
                                "description": "질문, 대답",
                            },
                        },
                        "required": ["name", "arguments"],
                    },
                },
            }
        ],
        tool_choice={"type": "function", "function": {"name": "extract_function_information"}}
    )
    arguments_json = response.choices[0].message.tool_calls[0].function.arguments
    function_info = json.loads(arguments_json)

    return function_info
