import sys
import os
# Add the project root to Python path   
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import asyncio
from typing import List, Any

from dotenv import load_dotenv, find_dotenv
from google.adk import Agent
from google.adk.tools import google_search

from a2a_servers.agent_servers.utils import generate_agent_task_manager, generate_agent_card
from a2a_servers.agents.adk_agent import ADKAgent
from a2a_servers.common.agent_task_manager import AgentTaskManager
from a2a_servers.common.server.server import A2AServer
from a2a_servers.common.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
)
from adk_agents_testing.mcp_tools.mcp_tool_search import return_sse_mcp_tools_search

load_dotenv(find_dotenv())

async def run_agent():
    AGENT_NAME = "google_search_agent"
    AGENT_DESCRIPTION = "An agent that handles search queries and can read pages online."
    HOST = "0.0.0.0"
    PORT = 11000
    AGENT_URL = f"http://{HOST}:{PORT}"
    AGENT_VERSION = "1.0.0"
    MODEL = 'gemini-2.5-flash'
    AGENT_SKILLS = [
        AgentSkill(
            id="GOOGLE_SEARCH",
            name="google_search",
            description="Handles search queries and can read pages online.",
        ),
    ]

    AGENT_CARD = generate_agent_card(
        agent_name=AGENT_NAME,
        agent_description=AGENT_DESCRIPTION,
        agent_url=AGENT_URL,
        agent_version=AGENT_VERSION,
        can_stream=False,
        can_push_notifications=False,
        can_state_transition_history=True,
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=AGENT_SKILLS,
    )

    gsearch_tools, g_search_exit_stack = await return_sse_mcp_tools_search()

    google_search_agent = ADKAgent(
        model=MODEL,
        name="google_search_agent",
        description="Handles search queries and can read pages online.",
        tools=gsearch_tools,
        instructions=(
            "You are an expert googler. Can search anything on google and read pages online."
        ),
    )

    task_manager = generate_agent_task_manager(
        agent=google_search_agent,
    )
    server = A2AServer(
        host=HOST,
        port=PORT,
        endpoint="/google_search_agent",
        agent_card=AGENT_CARD,
        task_manager=task_manager
    )
    print(f"Starting {AGENT_NAME} A2A Server on {AGENT_URL}")
    await server.astart()


if __name__ == "__main__":
    asyncio.run(
        run_agent()
    )
