from dotenv import load_dotenv
import os

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
from third_parties.linkedIn import scrape_linkedin_profile

# Load the environment variables from the .env file
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if __name__ == "__main__":

    print("Hello Langchain")

    summary_templates = """
    Given the LinkedIn information {information} about a person, I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_templates
    )

    # Example LLM setup
    llm = AzureChatOpenAI(
         deployment_name=deployment,
         openai_api_version="2024-02-01",
         azure_endpoint=endpoint,
         api_key=api_key,
     )

    # llm = ChatOllama(model="mistral")

    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/poonam-kumari-430b55229/"
    )

    if linkedin_data:
        chain = summary_prompt_template | llm | StrOutputParser()
        res = chain.invoke({"information": linkedin_data})
        print(res)
    else:
        print("No data found for the given LinkedIn profile.")
