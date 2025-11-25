from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # Loads OPENAI_API_KEY into the environment

def invoke_ai(system_message: str, user_message: str) -> str:
    """
    Generic function to invoke an AI model given a system and user message.
    Replace this if you want to use a different AI model.
    """

    # This is the fix:
    # Call OpenAI() with no arguments. It automatically finds
    # the 'OPENAI_API_KEY' you just loaded into the environment.
    client = OpenAI() 

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content