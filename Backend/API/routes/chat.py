import logging
from typing import Any, Dict

from fastapi import APIRouter, Request, HTTPException # Removed Body for this approach
from pydantic import BaseModel, Field                # Added Pydantic for body validation
from langchain_core.messages import HumanMessage
logger = logging.getLogger(__name__)

# --- Define Request Body Model ---
class ChatPayload(BaseModel):
    """Defines the expected JSON body for the chat request."""
    message: str = Field(..., description="The user's message content.")
    thread_id: str = Field(..., description="Identifier for the conversation thread.")

# --- Router Definition ---
chat_router = APIRouter()

@chat_router.post(
    "/", # Endpoint path remains "/" relative to the router's prefix
    summary="Send a message to the chat graph",
    description="Interacts with the LangGraph graph, maintaining conversation state using thread_id.",
    response_model=Dict[str, Any], # Explicitly define response type (usually the graph state dict)
)
async def chat(
    request: Request,           # Keep Request to access app state
    payload: ChatPayload,       # Use the Pydantic model to automatically parse the JSON body
) -> Dict[str, Any]:            # Return type is the final graph state dictionary
    """
    Handles incoming chat messages, invokes the graph, and returns the result.
    Uses the checkpointer associated with the graph via `thread_id` for statefulness.
    """
    # Access data from the validated payload object
    thread_id = payload.thread_id
    message = payload.message

    logger.info(f"Received chat message for thread_id='{thread_id}': '{message[:50]}...'") # Log truncated message

    # Prepare input data for the graph
    input_data = {
        "messages": [HumanMessage(content=message)]
    }

    # Prepare configuration for the checkpointer
    config = {"configurable": {"thread_id": thread_id}}

    try:
        # Access the compiled graph from application state
        # Ensure the graph object exists (should be guaranteed by lifespan if startup succeeded)
        if not hasattr(request.app.state, 'graph'):
             logger.error("Graph object not found in application state.")
             raise HTTPException(status_code=503, detail="Chat service is not available.")

        # Invoke the graph asynchronously using ainvoke
        result_state = await request.app.state.graph.ainvoke(input_data, config=config)

        logger.debug(f"Graph invocation successful for thread_id='{thread_id}'. Result: {result_state}")
        return result_state # Return the final state dictionary

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions directly (like the 503 above)
        raise http_exc
    except Exception as e:
        # Log the full error for server-side debugging
        logger.error(f"Error invoking graph for thread_id='{thread_id}': {e}", exc_info=True)
        # Raise a generic 500 error for the client
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the chat message."
        )