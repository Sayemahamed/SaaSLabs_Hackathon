from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from langgraph_swarm import create_handoff_tool, create_swarm
from dotenv import load_dotenv
from .tools import (
    fabricate_market_response,
    fabricate_website_response,
    fabricate_analytics_response,
)
from contextlib import _AsyncGeneratorContextManager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
import os
from .prompts import position_prompt, ab_test_prompt

load_dotenv()
import json
from pydantic import SecretStr

model = ChatOpenAI(
    api_key=SecretStr(os.getenv("OPENAI_API_KEY", "")),
    model="gpt-4.1",
    temperature=0,
)


position = create_react_agent(
    model=model,
    tools=[
        create_handoff_tool(
            agent_name="AB Tester",
            description="If user is interested in AB Testing, use this tool",
        ),
        fabricate_market_response,
    ],
    prompt=position_prompt,
    name="Positioning",
)
ab_tester = create_react_agent(
    model,
    tools=[
        create_handoff_tool(
            agent_name="Positioning",
            description="If user is interested in  Positioning & Brand Strategy , use this tool",
        ),
        fabricate_website_response,
        fabricate_analytics_response,
    ],
    prompt=ab_test_prompt,
    name="AB Tester",
)


swarm = create_swarm(agents=[ab_tester, position], default_active_agent="Positioning")

async def get_agent():
    cp_cm: _AsyncGeneratorContextManager[AsyncPostgresSaver, None] = (
        AsyncPostgresSaver.from_conn_string(os.getenv("DATABASE_URL", ""))
    )
    checkpointer: AsyncPostgresSaver = await cp_cm.__aenter__()

    try:
        await checkpointer.setup()
        return swarm.compile(checkpointer=checkpointer),cp_cm
    except Exception as e:
        await cp_cm.__aexit__(type(e), e, e.__traceback__)
        raise















# input = json.dumps(
#     {
#         "product_information": {
#             "product_name": "Mindful Brew",
#             "core_functionality": "A smart coffee maker that connects to an app to track user caffeine intake, analyzes reported sleep quality, and adjusts brew strength and timing recommendations to optimize focus and minimize negative side effects like jitters or sleep disruption.",
#             "target_audience": "Health-conscious professionals, tech enthusiasts, and coffee lovers (ages 25-55) interested in optimizing their energy levels, sleep, and overall well-being through personalized caffeine management.",
#             "problems_solved": [
#                 "Inconsistent energy levels from varying coffee strength.",
#                 "Difficulty tracking daily caffeine consumption accurately.",
#                 "Negative impacts of poorly timed caffeine intake on sleep quality.",
#                 "Over-reliance on caffeine leading to jitters or anxiety.",
#                 "Generic brewing doesn't adapt to individual daily needs or sensitivities.",
#             ],
#             "key_features": [
#                 "WiFi connectivity and companion app (iOS/Android).",
#                 "Personalized brew strength algorithm based on user input (sleep quality, schedule).",
#                 "Caffeine consumption tracking dashboard.",
#                 "Smart scheduling with optimal timing suggestions.",
#                 "Integration with popular sleep tracking apps/wearables (e.g., Fitbit, Apple Health).",
#                 "Premium build quality with precise temperature control.",
#                 "Multiple brew size options.",
#             ],
#             "pricing_model": "One-time hardware purchase with optional premium app subscription.",
#             "pricing_details": "Hardware MSRP: $249. Optional Pro Subscription (advanced analytics, recipes): $5.99/month or $59.99/year.",
#         }
#     }
# )

