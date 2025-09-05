from dotenv import load_dotenv
import os

load_dotenv()
from langchain_openai import AzureChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
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
    template = """
       given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username
       In Your Final answer only the person's username"""
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Twitter profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Twitter Page URL. If possible, return a valid URL string that contains 'twitter.com/'.",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    twitter_username = result["output"]
    return twitter_username


if __name__ == "__main__":
    print(lookup(name="Elon Musk"))
