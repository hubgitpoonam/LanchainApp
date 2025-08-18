import os

from dotenv import load_dotenv
from langchain.chains import llm
from langchain.chains.summarize.map_reduce_prompt import prompt_template
from pipenv.pep508checker import lookup


from tool.tool import get_profile_url_tavily

load_dotenv()

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import  Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)

from langchain import hub

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
def lookup(name: str) -> str:
    llm = AzureChatOpenAI(
        temperature=0,
        deployment_name=deployment,  # from your Azure portal
        api_version="2024-02-01"
    )


    template = """given the name {name_of_person} I want you to find a link to their Twitter/ X profile page, and extract from it their username
       In Your Final answer only the person's username
       which is extracted from: https://x.com/USERNAME"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name = "Crawl Google 4 twitter profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the twitter profile page",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
            {"input": prompt_template.format_prompt(name_of_person=name)}
        )

    linked_profile_url = result["output"]
    return linked_profile_url

if __name__ == "__main__":
    linedIn_url = lookup(name="EdenMacro")
    print(linedIn_url)