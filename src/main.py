from utils.llm import start_chat
from core.document_processor import read_and_process_faq
import chromadb
chroma_cilent = chromadb.Client()

if __name__ == "__main__":
    collection = chroma_cilent.get_or_create_collection(name="my_collection")
    clist = read_and_process_faq()
    for chunk in clist:
        collection.add(
            ids=chunk.metadata['category'],
            documents=chunk.page_content
        )
    query = input("Question: ")
    results = collection.query(
        query_texts=query,
        n_results=2
    )
    print(results)