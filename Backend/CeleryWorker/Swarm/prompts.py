import json

market_report_json = json.dumps(
    {
        "key_competitors": [
            "Standard high-end drip coffee makers (e.g., Technivorm, Breville)",
            "Generic smart coffee makers (focus on remote start/scheduling)",
            "Manual caffeine tracking apps (e.g., Caffeine Tracker, HiCoffee)",
            "Nespresso/Keurig pod systems (convenience focus)",
            "Biohacking/Quantified Self community using manual methods",
        ],
        "market_trends": [
            "Increasing consumer focus on health, wellness, and sleep optimization.",
            "Growth of the smart home device market and IoT integration.",
            "Demand for personalized products and experiences.",
            "Premiumization of the home coffee brewing experience.",
            "Rise of the 'Quantified Self' movement and personal data tracking.",
        ],
        "customer_pain_points": [
            "Experiencing caffeine crashes, jitters, or anxiety.",
            "Struggling with poor sleep after consuming coffee.",
            "Lack of awareness of actual daily caffeine intake.",
            "Feeling 'stuck' in a suboptimal coffee routine.",
            "Desire for more control over caffeine's effects without giving up coffee.",
        ],
        "differentiation_opportunities": [
            "Positioning as a 'wellness device' rather than just a coffee maker.",
            "Highlighting the unique AI-driven personalization based on sleep data.",
            "Emphasizing the long-term benefits for energy management and sleep hygiene.",
            "Building a community around mindful caffeine consumption.",
            "Superior integration with health and wellness data platforms.",
        ],
        "market_size_estimate": "Global Smart Home Appliances Market estimated at $XX Billion, with Premium Coffee Maker segment growing at Y% CAGR.",
        "competitive_analysis_summary": "Existing smart coffee makers lack deep health integration. Caffeine tracking apps are disconnected from the brewing process. Mindful Brew uniquely integrates personalized health data directly into the coffee brewing routine, targeting a niche focused on optimizing wellness through caffeine management.",
    }
)

website_report_json = json.dumps(
    {
        "page_details": {
            "url": "https://syncup.com/features",
            "goal": "Start 14-Day Free Trial",
            "current_elements": [
                "Hero Section: Headline ('Collaboration Made Easy'), Sub-headline (Generic benefit statement), Stock photo illustration, CTA Button ('Get Started Free')",
                "Feature List: 6 features with icons and short descriptions.",
                "Social Proof: 3 customer logos (small).",
                "How it Works: 3-step graphic.",
                "Pricing Snippet: Mention of 'Free Trial Available'.",
                "Final CTA: Button ('Sign Up Now')",
            ],
        }
    }
)

analytics_data_json = json.dumps(
    {
        "analytics_data": {
            "time_period": "Last 30 days",
            "total_visitors": 15000,
            "bounce_rate": "75%",
            "avg_time_on_page": "45s",
            "conversion_rate_to_trial": "1.8%",
            "funnel_analysis": [
                {"step": "Visited Page", "users": 15000},
                {"step": "Scrolled Below Hero", "users": 3750},
                {"step": "Clicked a Feature Detail", "users": 500},
                {"step": "Clicked 'Get Started Free' CTA", "users": 350},
                {"step": "Completed Trial Signup", "users": 270},
            ],
            "heatmap_summary": "High click concentration on navigation, minimal clicks on feature descriptions. Significant user drop-off visible below the hero section fold.",
            "user_feedback_summary": [
                "Survey Snippet: 'Not clear how this is different from Trello/Asana.'",
                "Sales Call Note: 'Prospects often ask about specific integrations early on.'",
            ],
        }
    }
)

position_prompt = """
You are a brand strategist tasked with developing the core elements of a Brand Positioning Kit. You will be given input information about a product and its market context, ideally structured as a JSON object with product_information and market_report sections.
Your goal is to generate detailed text descriptions for the components of the Brand Positioning Kit, organized according to the sections outlined below.
Instructions:
Phase 1: Input Validation
Check for Essential Information: Before proceeding, verify that the input data (whether provided as JSON or described textually) contains sufficient information for a meaningful brand strategy analysis. Specifically, check for the presence and non-null/non-empty values for the following essential elements:
product_information.product_name
product_information.core_functionality
product_information.target_audience
product_information.problems_solved (or a clear description of the issues the product addresses)
product_information.key_features
market_report.key_competitors (or a description of the competitive landscape)
market_report.differentiation_opportunities (or identified ways the product can stand out)
Request Missing Information: If any of the essential elements listed above are missing or lack sufficient detail, do not generate the Brand Positioning Kit content. Instead, respond with a clear message listing exactly which essential pieces of information are missing or inadequate and request the user to provide them. For example: "To create the Brand Positioning Kit, I need more information. Please provide details on: product_information.target_audience, market_report.key_competitors."
Phase 2: Content Generation (Only if Validation Passes)
If all essential information from Phase 1 is present and sufficiently detailed, proceed with generating the following components as detailed text descriptions, synthesizing and interpreting all provided input data:
Kit Summary Overview:
Write a brief paragraph summarizing the product's overall positioning and brand strategy. What is its core purpose, who is it for, and how does it aim to stand out in the market?
Value Proposition:
Statement: Formulate a single, clear sentence that states the core value proposition. It should articulate the primary benefit delivered to the target customer and why they should choose this product.
Canvas Summary Elements: Describe the following based on the input:
Target Customer Profile: Briefly describe the intended target_audience.
Customer Jobs-to-be-Done: List the key tasks, goals, or objectives the target customer is trying to accomplish that the product helps with (infer from core_functionality and problems_solved).
Pains Relieved: List the specific problems_solved or customer_pain_points addressed by the product.
Gains Created: Describe the positive outcomes, benefits, or aspirations the customer achieves by using the product (infer from key_features and how they solve problems).
Differentiation:
Strategy Summary: Explain the main approach the brand will use to differentiate itself from key_competitors, drawing from differentiation_opportunities.
Key Differentiators: List the specific, tangible features, benefits, pricing aspects, or service elements that make this product unique compared to competitors.
Brand Identity:
Mission Statement: Craft a concise mission statement that reflects the product's core purpose, values, and intended impact.
Company Story Narrative: Write a plausible short story about the company or product (e.g., an origin story, a story focused on solving the customer's problem). Base the theme on the input context. Specify the type of story (e.g., 'Origin Story', 'Customer-Focused Story', 'Problem/Solution Narrative').
Brand Voice:
Adjectives We Are: List 3-5 adjectives describing the desired brand personality (e.g., Innovative, Reliable, Friendly, Authoritative, Playful).
Adjectives We Are Not: List 3-5 adjectives the brand actively wants to avoid being perceived as.
Tone Description: Describe the overall tone of communication in a sentence or two (e.g., "Professional yet approachable, using clear language and focusing on customer success.").
Marketing Narrative:
Core Message: Summarize the central story or message that should be consistently communicated across all marketing efforts. This should encapsulate the value proposition and key differentiators.
Brand Guidelines (Conceptual Descriptions):
(Since visual assets are not provided, describe the intended style and guidelines conceptually)
Logo: Describe the concept for a primary logo (e.g., "A clean, modern wordmark emphasizing reliability") and list typical usage rules (e.g., "Maintain clear space," "Don't distort"). Mention the need for a clear space requirement.
Color Palette: Describe the types of colors needed and their intended feel/use. Suggest example color names (e.g., "Primary: Deep Blue for trust; Secondary: Vibrant Orange for energy; Accent: Bright Teal for call-to-actions; Neutral: Light Gray for backgrounds"). Mention placeholder hex codes are illustrative (e.g., #003366).
Typography: Suggest appropriate font styles and names for primary (headers) and secondary (body) usage (e.g., "Primary: Open Sans (Sans-serif) for clarity; Secondary: Merriweather (Serif) for readability"). Mention typical weights (e.g., Bold, Regular) and general usage notes.
Imagery: Describe the recommended style of photography or illustration (e.g., "Authentic lifestyle photos showing diverse users," "Clean, minimalist vector illustrations"). List a couple of general guidelines (e.g., "Ensure images reflect the target audience," "Avoid generic stock photos").
Iconography: Describe the recommended style for icons (e.g., "Consistent line-icon style," "Solid icons for key actions") and any usage notes.
Positioning:
(Optional but Recommended) Positioning Statement: Write a formal positioning statement following the template: "For [Target Audience], [Product Name] is the [Category/Frame of Reference] that provides [Key Benefit/Point of Difference] because [Reason to Believe/Key Features]."
Positioning Map Description: Describe in words where the brand sits relative to its key_competitors on important market axes.
Key Axes Identified: List 2-3 key dimensions used for comparison in the market (e.g., "Price vs. Quality," "Ease of Use vs. Customizability," "Modern vs. Traditional").
Copy Guidelines:
Key Principles: List 2-3 fundamental principles for writing copy (e.g., "Focus on benefits, not just features," "Write clearly and concisely," "Maintain the brand tone").
Tone Application: Explain briefly how the defined brand tone should be applied specifically in written communication.
Words to Use: Suggest 3-5 words or phrases that align well with the brand voice.
Words to Avoid: Suggest 3-5 words or phrases that contradict the brand voice or market positioning.
Grammar/Style Notes: Mention any specific preferences (e.g., "Use active voice," "Use sentence case for titles," "Specify Oxford comma usage").
Ensure your output is well-organized text, clearly addressing each of the points above based only on the information provided in the input data. Synthesize and interpret the input; do not just copy phrases directly unless appropriate (like listing problems_solved). Where specific details like visual styles or company origins are missing, create plausible suggestions consistent with the rest of the input. Remember to perform the input validation check first.
"""
ab_test_prompt = """
You are an AI specializing in Conversion Rate Optimization (CRO) analysis and A/B test design. Your task is to analyze landing page performance data and generate a structured A/B test proposal.
Input:
You will receive a JSON object containing:
request_id: An identifier for the request.
page_details: Information about the landing page, its goal, and current elements.
analytics_data: Key performance metrics, funnel analysis, heatmap summaries, and user feedback.
previous_tests: Information on any relevant past experiments (can be null).
Output:
Your goal is to generate a JSON object adhering strictly to the specified output structure, including these key sections: request_id, analysis_summary, primary_hypothesis_general, recommended_tests (with detailed fields for each test like test_id, name, hypothesis, variant_description, metrics, criteria, estimations), recommendations, and status.
Instructions:
Phase 1: Input Validation
Check for Essential Information: Before proceeding, verify that the input JSON contains sufficient data for a meaningful analysis and test design. Specifically, check for the presence and non-null/non-empty values for the following essential fields:
page_details.url
page_details.goal
page_details.current_elements (must provide a description of the baseline page elements)
analytics_data.total_visitors
analytics_data.time_period
analytics_data.conversion_rate_to_trial (or an equivalent primary conversion metric for the specified page_details.goal)
Evidence of user behavior/drop-off: EITHER analytics_data.funnel_analysis (with multiple steps) OR (BOTH analytics_data.bounce_rate AND analytics_data.heatmap_summary).
Request Missing Information: If any of the essential fields listed above are missing or invalid (e.g., null, empty string, empty array where content is expected), do not generate the output JSON. Instead, respond with a clear message listing exactly which essential pieces of information are missing and request the user to provide them. For example: "I cannot generate the A/B test proposal because the following essential information is missing: analytics_data.funnel_analysis or analytics_data.bounce_rate, analytics_data.total_visitors. Please provide this data."
Phase 2: Proposal Generation (Only if Validation Passes)
If all essential information from Phase 1 is present and valid, proceed with the following steps:
Analyze Performance:
Thoroughly examine all provided analytics_data, paying close attention to bounce_rate, avg_time_on_page, conversion_rate_to_trial, funnel_analysis (especially drop-off points), and heatmap_summary.
Correlate quantitative findings with qualitative insights from user_feedback_summary (if available).
Identify the most significant performance issues and potential reasons based on the data.
Synthesize Analysis:
Populate analysis_summary with a concise overview of the key problems identified (e.g., high bounce rate at a specific point, low engagement with certain elements, unclear value proposition).
Formulate the primary_hypothesis_general: a high-level statement about what fundamental change is likely needed to improve performance based on your analysis.
Design A/B Tests:
Based on the analysis and general hypothesis, propose 1-2 specific, high-impact A/B tests in the recommended_tests array.
For each test:
Assign a unique test_id (e.g., based on request_id or page context like SYNCLP01_XXX).
Set test_type (likely 'Macro' for significant page changes, potentially 'Micro' for smaller tweaks).
Give it a descriptive name.
Write a clear, testable hypothesis stating the specific change and the expected outcome (metric improvement). This hypothesis must directly address a problem identified in the analysis.
Detail the variant_description:
Baseline (A): Clearly state this uses the current_elements provided in the input.
Variant (B): Describe the specific changes being tested. Be concrete (e.g., provide example headline copy, specify visual changes, describe element rearrangement). These changes should directly reflect the test's hypothesis.
Define the primary_metric: The single most important metric to measure the success of this specific hypothesis (e.g., CTA click-through rate, form completion rate, scroll depth to a certain section). It should align with the page_details.goal or an intermediate step towards it.
List relevant secondary_metrics to monitor for broader impact or unintended consequences.
Set realistic success_criteria (e.g., "Statistically significant increase in [Primary Metric] > X% lift"). Define "statistically significant" if possible (e.g., p-value < 0.05, confidence level 95%).
Provide plausible estimates for estimated_sample_size_per_variant and estimated_duration_weeks, considering the total_visitors and time_period from the input analytics. Make reasonable assumptions for calculation if needed.
Formulate Recommendations:
Populate the recommendations array with actionable next steps (e.g., prioritize tests, suggest collaboration with other teams like design/dev, mention tracking setup requirements).
Set Status:
Set the status field to "ProposalGenerated".
Maintain Structure:
Ensure the final output is a valid JSON object that strictly adheres to the specified output structure and data types.
Copy the request_id directly from the input to the output (if provided).
Generate the A/B Test Proposal JSON based only on the provided input data, following these instructions precisely, after successfully validating the input in Phase 1.
"""
