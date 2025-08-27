from llama_index.llms.azure_openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = AzureOpenAI(
    engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # deployment name from Azure OpenAI Studio
    model="gpt-35-turbo-16k",  # model name
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
response = llm.complete("The sky is a beautiful blue and")
print(response)