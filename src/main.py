from utils.llm import UserQuery, chat

def main():
    prompt = input("Người dùng: ")
    user_query = UserQuery(name="million", query=prompt, timestamp=123.4)
    chat(user_query)

if __name__ == "__main__":
    main()