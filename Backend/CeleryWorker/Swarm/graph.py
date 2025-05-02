from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from rich import print

from langgraph_swarm import create_handoff_tool, create_swarm
from dotenv import load_dotenv
from tools import (
    fabricate_market_response,
    fabricate_website_response,
    fabricate_analytics_response,
)
import os
from prompts import position_prompt, ab_test_prompt

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


swarm = create_swarm(agents=[ab_tester, position], default_active_agent="AB Tester")
memory = InMemorySaver()

input = json.dumps(
    {
        "request_id": "syncup_lp_test_01",
        "page_details": {
            "url": "https://syncup.com/features",
            "goal": "Start 14-Day Free Trial",
            "current_elements": [
                "Hero Section: Headline ('Collaboration Made Easy'), Sub-headline (Generic benefit statement), Stock photo illustration, CTA Button ('Get Started Free')",
                "Feature List: 6 features with icons and short descriptions.",
                "Social Proof: 3 customer logos (small).",
                "How it Works: 3-step graphic.",
                "Pricing Snippet: Mention of 'Free Trial Available'.",
                "Final CTA: Button ('Sign Up Now')"
            ]
        },
        "analytics_data": {
            "time_period": "Last 30 days",
            "total_visitors": 15000,
            "bounce_rate": "75%",
            "avg_time_on_page": "45s",
            "conversion_rate_to_trial": "1.8%",
            "funnel_analysis": [
                { "step": "Visited Page", "users": 15000 },
                { "step": "Scrolled Below Hero", "users": 3750 }, # Significant drop-off (75% leave)
                { "step": "Clicked a Feature Detail", "users": 500 },
                { "step": "Clicked 'Get Started Free' CTA", "users": 350 },
                { "step": "Completed Trial Signup", "users": 270 } # 1.8% of initial visitors
            ],
            "heatmap_summary": "High click concentration on navigation, minimal clicks on feature descriptions. Significant user drop-off visible below the hero section fold.",
            "user_feedback_summary": [
                "Survey Snippet: 'Not clear how this is different from Trello/Asana.'",
                "Sales Call Note: 'Prospects often ask about specific integrations early on.'"
            ]
        },
        "previous_tests": None 
    }
)

swarm = swarm.compile()

resp=swarm.invoke(input={"messages": [HumanMessage(content=input)]})
print(
resp["messages"][-1].content
)















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

