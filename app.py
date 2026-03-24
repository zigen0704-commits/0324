import os
from openai import AzureOpenAI

from flask import Flask, request, render_template

app = Flask(__name__)

endpoint = os.getenv('OpenAI_ENDPOINT')
model_name = os.getenv('OpenAI_DEPLOY_NAME')
subscription_key = os.getenv('OpenAI_API_KEY')
deployment = "gpt-4o-mini"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?",
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

print(response.choices[0].message.content)


if __name__ == '__main__':
    # 開發用；部署用 gunicorn（見下方）
    app.run(host='0.0.0.0', debug=False)
