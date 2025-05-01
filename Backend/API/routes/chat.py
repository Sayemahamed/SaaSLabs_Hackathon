from fastapi import APIRouter,Request
chat_router = APIRouter()
@chat_router.post(
    "/chat",
    summary="Send a message to the chat graph", # Updated summary
    description="Interacts with the LangGraph graph, maintaining conversation state using thread_id.", # Updated description
)
async def chat(
    request: Request,
    payload: ChatRequest = Body(...),
) -> Dict[str, Any]:
    """
    Handles incoming chat messages, invokes the graph, and returns the result.
    Uses the checkpointer associated with the graph via `thread_id` for statefulness.
    """
    thread_id = payload.thread_id or "default_single_user_thread"
    user_message = payload.message

    logger.info(f"Received chat message for thread_id='{thread_id}': '{user_message}'")

    input_data = {
        "messages": [HumanMessage(content=user_message)]
    }
    config = {"configurable": {"thread_id": thread_id}}

    try:
        # **** CHANGED: Log message and invocation target ****
        logger.debug(f"Invoking graph for thread_id='{thread_id}' with config: {config}")
        # **** CHANGED: await graph.ainvoke(...) ****
        result_state = await graph.ainvoke(input_data, config=config)
        # **** CHANGED: Log message ****
        logger.info(f"Graph invocation successful for thread_id='{thread_id}'.")
        logger.debug(f"Final state for thread_id='{thread_id}': {result_state}")

        return result_state

    except Exception as e:
        # **** CHANGED: Log message ****
        logger.error(f"Error invoking graph for thread_id='{thread_id}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the chat message."
        )