from utils.llm import start_chat
from core.document_processor import read_and_process_faq

if __name__ == "__main__":
    # start_chat()
    clist = read_and_process_faq()
    print(clist)