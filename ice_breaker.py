from dotenv import load_dotenv
import os

from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from OutputParser import summary_parser
from third_parties.linkedIn import scrape_linkedin_profile
from agent.LinkedIn_agent_package import lookup as linkedin_lookup_agent
from third_parties.fetchtweepy import scrape_user_tweets

# Load env
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def ice_breaker_with(name: str, twitter_handle: str = None):
    # 1. LinkedIn Lookup
    linkedin_username = linkedin_lookup_agent(name=name)

    if "linkedin.com/in/" not in linkedin_username:
        linkedin_username = "https://www.linkedin.com/in/poonam-kumari-430b55229/"

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    # 2. Tweets (use mock if API fails)
    twitter_data = []
    if twitter_handle:
        try:
            twitter_data = scrape_user_tweets(username=twitter_handle, num_tweet=5)
        except Exception as e:
            print(f"Error fetching tweets for {twitter_handle}: {e}")
            print(" Falling back to mock tweets...")
            twitter_data = scrape_user_tweets(username=twitter_handle, num_tweet=5, mock=True)

    # 3. Prompt (keep variables as placeholders for PromptTemplate)
    summary_templates = """
    Given the following information, create:
    1. A short professional summary from LinkedIn.
    2. Two interesting facts about them.
    3. If Twitter data is available, summarize 2 insights from their recent tweets.

    LinkedIn Data:
    {linkedin_info}

    Twitter Data:
    {twitter_info}

    Formatting Instructions:
    {format_instruction}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_info", "twitter_info"],
        template=summary_templates,
        partial_variables={"format_instruction": summary_parser.get_format_instructions()}
    )

    # 4. LLM
    llm = AzureChatOpenAI(
        deployment_name=deployment,
        openai_api_version="2024-02-01",
        azure_endpoint=endpoint,
        api_key=api_key,
    )

    # Use structured parser
    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke({
        "linkedin_info": linkedin_data,
        "twitter_info": twitter_data
    })

    print(res)


if __name__ == "__main__":
    print("Ice Breaker Enter")
    # Example with both LinkedIn + Twitter
    ice_breaker_with(name="PoonamKumari", twitter_handle="EdenEmarco177")
