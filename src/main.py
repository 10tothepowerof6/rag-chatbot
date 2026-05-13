from pydantic import BaseModel

class UserQuery(BaseModel):
    name: str
    query: str
    timestamp: float

def main():
    user = UserQuery(name="million", query="What's RAG?", timestamp="123456789")
    
    print(user.timestamp)
    print(type(user.timestamp))
    print(user.model_dump_json())

if __name__ == "__main__":
    main()