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
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                              Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL. If possible, return a valid URL string that contains 'linkedin.com/'.",
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

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    print(lookup(name="Eden Marco Udemy"))
