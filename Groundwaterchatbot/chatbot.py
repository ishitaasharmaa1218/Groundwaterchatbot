import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_bot(query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful groundwater expert assistant."},
            {"role": "user", "content": query}
        ]
    )
    
    return response.choices[0].message.content