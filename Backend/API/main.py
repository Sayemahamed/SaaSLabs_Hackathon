import logging
from contextlib import asynccontextmanager

# Assuming API is a package/directory at the same level or in sys.path
from API.config import settings  # Import settings for potential use
from API.db import init_db
from API.middlewares import LoggingMiddleware
from API.routes import auth_router, user_router,chat_router
from fastapi import FastAPI
from API.agent import get_agent
from fastapi.middleware.cors import CORSMiddleware
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan hook to initialize resources and clean them up on shutdown.
    Initializes database and agent resources.
    """
    logger.info("Application startup sequence initiated...")
    print("[green]Starting up...")  
    # app.state.swarm = swarm.compile(checkpointer=PostgresSaver.from_conn_string(
    #     "postgresql://postgres:postgres@localhost:5432/postgres"
    # ))
    try:
        graph, pool_cm = await get_agent()
        app.state.graph = graph
        app.state.graph_cm = pool_cm
        logger.info("Agent pool graph initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize agent pool graph: {e}", exc_info=True)
    # Initialize Database
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        # Decide if the app should fail to start if DB is critical
        raise RuntimeError("Failed to initialize database") from e

    yield  # Application runs here

    # --- Shutdown Sequence ---
    logger.info("Application shutdown sequence initiated...")
    print("[green]Shutting down...")  
    if hasattr(app.state, "pool_cm") and app.state.pool_cm:
        try:
            await app.state.pool_cm.__aexit__(None, None, None)
            logger.info("Agent pool context manager closed successfully.")
        except Exception as e:
            logger.error(
                f"Error closing agent pool context manager: {e}", exc_info=True
            )
            print(
                f"[red]Error closing pool: {e}"
            )  # Keep rich print if preferred for dev
    else:
        logger.warning("Agent pool context manager not found or already closed.")


    logger.info("Application shutdown complete.")


# --- FastAPI App Initialization ---
API_VERSION = "v1"

app = FastAPI(lifespan=lifespan)

# Add logging middleware

app = FastAPI(
    title="SaaS labs",
    lifespan=lifespan,
    version=API_VERSION,
    description="",
)

# --- Middleware ---
# WARNING: allow_origins=["*"] is insecure for production.
# Replace "*" with the list of specific origins allowed to access your API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # SECURITY RISK: Restrict in production
    allow_credentials=True,
    allow_methods=[
        "*"
    ],  # Consider restricting methods (e.g., ["GET", "POST", "PUT", "DELETE"])
    allow_headers=["*"],  # Consider restricting headers if needed
)

app.add_middleware(LoggingMiddleware)
# --- API Routers ---
api_prefix = f"/{API_VERSION}"

app.include_router(user_router, prefix=f"{api_prefix}/user", tags=["User"])
app.include_router(auth_router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(chat_router, prefix=f"{api_prefix}/chat", tags=["Chat"])

# Root endpoint (optional)
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to Price Pilot API {API_VERSION}"}
