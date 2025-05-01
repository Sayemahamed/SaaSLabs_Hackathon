from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from Backend.CeleryWorker.CMO.Nodes import call_agent, decider, summarize
from Backend.CeleryWorker.CMO.state import State

builder = StateGraph(state_schema=State)

builder.add_node(node="agent", action=call_agent)
builder.add_node(node="summarize", action=summarize)

builder.add_conditional_edges(source=START, path=decider)
builder.add_edge(start_key="summarize", end_key="agent")
builder.add_edge(start_key="agent", end_key=END)
graph = builder.compile()
# with PostgresSaver.from_conn_string(
#     "postgresql://postgres:postgres@localhost:5432/postgres"
# ) as memory:
#     graph: CompiledStateGraph = builder.compile(
#         interrupt_before=["summarize"], checkpointer=memory
#     )

# graph.invoke(
#     {"messages": [HumanMessage(content="Hello, I am Sayem")]},
#     {"configurable": {"thread_id": 1}},
# )
# graph.invoke(
#     {"messages": [HumanMessage(content="can You Help me with maths")]},
#     {"configurable": {"thread_id": 1}},
# )
# graph.invoke(
#     {"messages": [HumanMessage(content="who are You?")]},
#     {"configurable": {"thread_id": 1}},
# )
