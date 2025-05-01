from ast import mod
import re
from urllib import response
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from .prompts import analytics_data_json, market_report_json, website_report_json
from langchain_core.messages import SystemMessage
from rich import print
from pydantic import SecretStr

load_dotenv()
client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY",
        "",
    )
)
model = ChatOpenAI(
    temperature=0,
    model="gpt-4.1",
    api_key=SecretStr(
        os.getenv(
            "OPENAI_API_KEY",
            "",
        )
    ),
)


def getData(query: str):
    """
    Send a query to the OpenAI web search tool and return the results as a string.

    Args:
        query (str): The query to send to the search tool.

    Returns:
        str: The results of the search as a string.
    """
    response = client.responses.create(
        model="gpt-4.1",
        tools=[
            {
                "type": "web_search_preview",
                "search_context_size": "low",
            }
        ],
        input=query,
    )
    return response.output_text


def fabricate_analytics_response(topic: str):    
    """
    Generate a fake analytics report for the given topic.

    Args:
        topic (str): The topic to generate an analytics report for.

    Returns:
        str: The results of the search as a string.
    """
    agent = create_react_agent(
        model=model,
        tools=[getData],
        prompt=f"Generate fake data for analytics report for a website {topic}, the following analytics data as reference {analytics_data_json} keep the data as rich as possible and keep them related to {topic}",
    )
    response=agent.invoke({"messages": [SystemMessage(content=topic)]})
    return response["messages"][-1].content


def fabricate_market_response(topic: str):
    """
    Generate a fake market report for the given topic.

    Args:
        topic (str): The topic to generate a market report for.

    Returns:
        str: The results of the search as a string.
    """
    agent = create_react_agent(
        model=model,
        tools=[getData],
        prompt=f"Generate fake market report for a website {topic}, the following market report as reference {market_report_json} keep the data as rich as possible and keep them related to {topic}",
    )
    response=agent.invoke({"messages": [SystemMessage(content=topic)]})
    return response["messages"][-1].content


def fabricate_website_response(topic: str):
    """
    Generate a fake website report for the given topic.

    Args:
        topic (str): The topic to generate a website report for.

    Returns:
        str: The generated website report as a string.
    """
    agent = create_react_agent(
        model=model,
        tools=[getData],
        prompt=f"Generate fake website report for a website {topic}, the following website report as reference {website_report_json} keep the data as rich as possible and keep them related to {topic}",
    )
    response=agent.invoke({"messages": [SystemMessage(content=topic)]})
    return response["messages"][-1].content


# fabricate_analytics_response("Ecommerce")
# fabricate_market_response("Ecommerce")
# fabricate_website_response("Ecommerce")
