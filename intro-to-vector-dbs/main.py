import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import OllamaEmbeddings

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


load_dotenv()


if __name__ == "__main__":
    print(" Retrieving...")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
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

    query = "what is Pinecone in machine learning?"
    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input={})
    print(result.content)

    vectorstore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"], embedding=embeddings
    )
    retrival_qa_chat_promt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrival_qa_chat_promt)
    retrival_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )

    result = retrival_chain.invoke(input={"input": query})

    print(result)
