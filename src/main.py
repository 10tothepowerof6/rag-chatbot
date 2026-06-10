from core.vector_store import add_document, query_document
from core.document_processor import read_and_process_faq

if __name__ == "__main__":
    data = read_and_process_faq()
    add_document(data)
    query_result = query_document("My order status did not update yet")
    print(query_result)