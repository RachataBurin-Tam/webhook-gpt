#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai

openai.api_type = "azure"
openai.api_base = "https://ingenio-openai-east.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "cf1eaaea9f40498f9eccf4bafc89f3de"


message_text = [{"role":"system",
                 "content":"You are an AI assistant that helps people find information in Thai language"}]


def ask_azure_gpt(question):
    response = openai.ChatCompletion.create(
                    engine="bbik-demo-gpt35",
                    messages = message_text,
                    temperature=0.7,
                    max_tokens=800,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                    )

    return response["choices"][0]["text"].strip()
