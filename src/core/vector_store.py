from google import genai
from google.genai import types
from core.document_processor import Chunk
from config.settings import GEMINI_API_KEY, EMBEDDING_MODEL, VECTOR_DATA_PATH
import chromadb

chroma_client = chromadb.PersistentClient(path=VECTOR_DATA_PATH)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def embed_retrieval_documents(content: list[str]):
    """
    Generate embedding vectors for a list of document texts

    Args:
        content (list[str]): A list of strings representing the document contents
                            that need to be embedded.

    Returns:
        list[list[float]]: A list of embedding vectors for each document content
    """
    result = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=content,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    all_embedding_vectors = [emb.values for emb in result.embeddings]
    return all_embedding_vectors

def embed_retrieval_query(content: str):
    """
    Generate embedding vectors for a single query

    Args:
        content (str): The search query
    
    Returns:
        list[float]: An embedding vector of the search query
    """
    result = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=content,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    return result.embeddings[0].values

def add_document(data: list[Chunk]):
    """
    Embed document chunks and store/update them in the ChromaDB collection.

    Args:
        data (list[Chunk]): A list of document chunks that need to be embedded
                            and stored/updated
    """
    collection = chroma_client.get_or_create_collection(name="embedded_documents")
    id_list: list[str] = []
    document_list: list[str] = []
    metadata_list: list[dict] = []

    for i, chunk in enumerate(data):
        id_list.append(f"{chunk.metadata['source_file']}_{i}")
        document_list.append(chunk.page_content)
        metadata_list.append(chunk.metadata)
    
    embedding_list=embed_retrieval_documents(document_list)
    collection.upsert(
        ids=id_list,
        embeddings=embedding_list,
        documents=document_list,
        metadatas=metadata_list
    )

def query_document(query_text: str):
    """
    Search for similar document chunks in ChromaDB based on the user's query.

    Args:
        query_text (str): The search query

    Returns:
        dict: A dictionary containing matching documents, distances and metadatas from ChromaDB
    """
    collection = chroma_client.get_or_create_collection(name="embedded_documents")
    query_embedding = embed_retrieval_query(query_text)
    query_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    return query_results
