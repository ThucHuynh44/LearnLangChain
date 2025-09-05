import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()

if __name__ == "__main__":
    print("Starting the ingestion process...")
    # Load environment variables
    # Lấy thư mục chứa ingestion.py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Ghép đường dẫn đến file cần load
    file_path = os.path.join(BASE_DIR, "mediumblog1.txt")

    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    print("splitting the documents...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    print(f"created {len(texts)} chunks of data")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print("ingesting ...")
    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.getenv("INDEX_NAME")
    )
    print("finished ingesting the data")
