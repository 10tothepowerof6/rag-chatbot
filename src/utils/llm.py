from google import genai
from google.genai import types
from pydantic import BaseModel
from config.settings import DEFAULT_MODEL, GEMINI_API_KEY, SYSTEM_INSTRUCTION, TEMPERATURE


client = genai.Client(api_key=GEMINI_API_KEY)

class UserQuery(BaseModel):
    name: str
    query: str
    timestamp: float

def start_chat():
    """
    Start an interactive command-line chat session with the Gemini model

    This function initializes a chat session that runs infinitely to accept
    user input and print out the model's response until the user types 'exit'.
    """
    chat = client.chats.create(
        model=DEFAULT_MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=TEMPERATURE
        )
    )
    while (True):
        prompt = input("User: ")
        if prompt.lower() == 'exit':
            break
        user_query = UserQuery(name="million", query=prompt, timestamp=123.4)
        response = chat.send_message(user_query.query)
        print("Customer Support: " + response.text)
    print("Customer Support: Good bye and hope to see you soon!")
    client.close()

def chat(user_query: UserQuery):
    """
    Generate a single-turn response for a structured user query.

    Args:
        user_query (UserQuery): A Pydantic model containing the 
                                query text and query metadata.
    """
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=user_query.query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=TEMPERATURE
        )
    )
    print("Customer Support: " + response.text)
    client.close()
