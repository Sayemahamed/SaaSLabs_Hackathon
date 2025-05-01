import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

load_dotenv()
client = TavilyClient(os.getenv("TAVILY_API_KEY", ""))

app = FastMCP("Tavily")


@app.tool()
def search(query: str):
    return client.search(
        query=query,
        search_depth="advanced",
        max_results=10,
        time_range="year",
        include_answer="advanced",
    )


if __name__ == "__main__":
    app.run(transport="sse")
