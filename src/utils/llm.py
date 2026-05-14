import os
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = "Bạn là một nhân viên hỗ trợ khách hàng thông minh và tận tâm của công ty công nghệ FPT, Trả lời ngắn gọn, súc tích và chuyên nghiệp."
TEMPERATURE = 0.0

class UserQuery(BaseModel):
    name: str
    query: str
    timestamp: float

def chat(user_query: UserQuery):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=user_query.query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=TEMPERATURE
        )
    )
    print("CSKH: " + response.text)

if __name__ == "__main__":
    user_query = UserQuery(name="million", query="Hello", timestamp=123.4)
    chat(user_query)