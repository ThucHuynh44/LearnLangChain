import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import AzureChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain_community.embeddings import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    print("hi")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Ghép đường dẫn đến file cần load
    pdf_path = os.path.join(BASE_DIR, "Project_file.pdf")
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n"
    )
    docs = text_splitter.split_documents(documents=documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index_react")

    new_vectorstore = FAISS.load_local(
        "faiss_index_react", embeddings, allow_dangerous_deserialization=True
    )
    llm = AzureChatOpenAI(
        deployment_name=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        ),  # Tên deployment trong Azure
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  # VD: "2023-07-01-preview"
        azure_endpoint=os.getenv(
            "AZURE_OPENAI_ENDPOINT"
        ),  # VD: "https://xxx.openai.azure.com/"
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        temperature=0,
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrieval_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(), combine_docs_chain
    )

    res = retrieval_chain.invoke({"input": "sumarize problem in 3 sentences"})
    print(res["answer"])
