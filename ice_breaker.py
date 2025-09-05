import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from typing import Tuple
from output_parsers import summary_parser, Summary


load_dotenv()


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkein_username = lookup(name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkein_username)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username)

    summary_template = """
    given the information about a person from linkedin {information},
    and their latest twitter posts {twitter_posts} I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
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

    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(
        input={"information": linkedin_data, "twitter_posts": tweets}
    )

    print("\n\n photoUrl:", linkedin_data.get("photoUrl"))
    return res, linkedin_data.get("photoUrl")


if __name__ == "__main__":
    print(ice_break_with(name="Eden Marco Udemy"))
