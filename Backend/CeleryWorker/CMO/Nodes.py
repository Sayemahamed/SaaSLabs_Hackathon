import logging
import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from prompts import (
    marketing_prompt,
    positioning_prompt,
    acquisition_prompt,
    content_prompt,
    onboarding_prompt,
    growth_prompt,
)
from pydantic import SecretStr
from state import State
from tools import marketing_config

load_dotenv()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=SecretStr(secret_value=os.getenv("OPENAI_API_KEY", "")),
)

llm = llm.with_fallbacks(
    [
        ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            temperature=0,
            api_key=SecretStr(secret_value=os.getenv("GEMINI_API_KEY", "")),
        )
    ]
)


def CMO(state: State) -> State:
    pass


def orchestrator(
    state: State,
) -> Literal[
    "market",
    "positioning",
    "acquisition",
    "content",
    "onboarding",
    "growth",
    "cmo",
    "__end__",
]:
    response = llm.invoke([SystemMessage(content=marketing_prompt)] + state["messages"])
    if not isinstance(response.content, str):
        return "__end__"
    words = response.content.lower().split(" ")
    keywords = [
        "market",
        "positioning",
        "acquisition",
        "content",
        "onboarding",
        "growth",
        "cmo",
    ]
    for keyword in keywords:
        if keyword in words:
            return keyword  # type: ignore
    return "__end__"


async def marketing(state: State) -> State:
    logger.info("Entering Market Intelligence node")
    try:
        async with MultiServerMCPClient(marketing_config) as client:  # type: ignore
            agent_tools = client.get_tools()
            agent: CompiledGraph = create_react_agent(model=llm, tools=agent_tools)
            logger.debug(
                f"Market Intelligence agent initialized with tools: {[t.name for t in agent_tools]}"
            )

            response = await agent.ainvoke(
                {
                    "messages": [SystemMessage(content=marketing_prompt)]
                    + state["messages"]
                }
            )
            return {"messages": [AIMessage(content=response["messages"][-1].content)]}
    except Exception as e:
        logger.error(f"Error in Market Intelligence node: {e}", exc_info=True)
        return {
            "messages": [
                SystemMessage(content=f"Error in Market Intelligence: {str(e)}")
            ]
        }


async def positioning(state: State) -> State:
    logger.info("Entering Positioning node")
    try:
        async with MultiServerMCPClient(positioning_config) as client:  # type: ignore
            agent_tools = client.get_tools()
            agent: CompiledGraph = create_react_agent(model=llm, tools=agent_tools)
            logger.debug(
                f"Positioning agent initialized with tools: {[t.name for t in agent_tools]}"
            )

            response = await agent.ainvoke(
                {
                    "messages": [SystemMessage(content=positioning_prompt)]
                    + state["messages"]
                }
            )
            return {"messages": [AIMessage(content=response["messages"][-1].content)]}
    except Exception as e:
        logger.error(f"Error in Positioning node: {e}", exc_info=True)
        return {"messages": [SystemMessage(content=f"Error in Positioning: {str(e)}")]}


async def acquisition(state: State) -> State:
    logger.info("Entering Acquisition node")
    try:
        async with MultiServerMCPClient(acquisition_config) as client:  # type: ignore
            agent_tools = client.get_tools()
            agent: CompiledGraph = create_react_agent(model=llm, tools=agent_tools)
            logger.debug(
                f"Acquisition agent initialized with tools: {[t.name for t in agent_tools]}"
            )

            response = await agent.ainvoke(
                {
                    "messages": [SystemMessage(content=acquisition_prompt)]
                    + state["messages"]
                }
            )
            return {"messages": [AIMessage(content=response["messages"][-1].content)]}
    except Exception as e:
        logger.error(f"Error in Acquisition node: {e}", exc_info=True)
        return {"messages": [SystemMessage(content=f"Error in Acquisition: {str(e)}")]}


async def content(state: State) -> State:
    logger.info("Entering Content node")
    try:
        async with MultiServerMCPClient(content_config) as client:  # type: ignore
            agent_tools = client.get_tools()
            agent: CompiledGraph = create_react_agent(model=llm, tools=agent_tools)
            logger.debug(
                f"Content agent initialized with tools: {[t.name for t in agent_tools]}"
            )

            response = await agent.ainvoke(
                {
                    "messages": [SystemMessage(content=content_prompt)]
                    + state["messages"]
                }
            )
            return {"messages": [AIMessage(content=response["messages"][-1].content)]}
    except Exception as e:
        logger.error(f"Error in Content node: {e}", exc_info=True)
        return {"messages": [SystemMessage(content=f"Error in Content: {str(e)}")]}


async def onboarding(state: State) -> State:
    logger.info("Entering Onboarding node")
    try:
        async with MultiServerMCPClient(onboarding_config) as client:  # type: ignore
            agent_tools = client.get_tools()
            agent: CompiledGraph = create_react_agent(model=llm, tools=agent_tools)
            logger.debug(
                f"Onboarding agent initialized with tools: {[t.name for t in agent_tools]}"
            )

            response = await agent.ainvoke(
                {
                    "messages": [SystemMessage(content=onboarding_prompt)]
                    + state["messages"]
                }
            )
            return {"messages": [AIMessage(content=response["messages"][-1].content)]}
    except Exception as e:
        logger.error(f"Error in Onboarding node: {e}", exc_info=True)
        return {"messages": [SystemMessage(content=f"Error in Onboarding: {str(e)}")]}


async def growth(state: State) -> State:
    logger.info("Entering Growth node")
    try:
        async with MultiServerMCPClient(growth_config) as client:  # type: ignore
            agent_tools = client.get_tools()
            agent: CompiledGraph = create_react_agent(model=llm, tools=agent_tools)
            logger.debug(
                f"Growth agent initialized with tools: {[t.name for t in agent_tools]}"
            )

            response = await agent.ainvoke(
                {"messages": [SystemMessage(content=growth_prompt)] + state["messages"]}
            )
            return {"messages": [AIMessage(content=response["messages"][-1].content)]}
    except Exception as e:
        logger.error(f"Error in Growth node: {e}", exc_info=True)
        return {"messages": [SystemMessage(content=f"Error in Growth: {str(e)}")]}
