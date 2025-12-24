
import sys
import os
# Add the project root to Python path   
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import asyncio
from dotenv import load_dotenv, find_dotenv

from a2a_servers.agent_servers.utils import generate_agent_card, generate_agent_task_manager
from a2a_servers.agents.adk_agent import ADKAgent
from a2a_servers.common.server.server import A2AServer
from a2a_servers.common.types import (
    AgentSkill,
)
from adk_agents_testing.mcp_tools.mcp_tool_stocks import return_sse_mcp_tools_stocks

load_dotenv(find_dotenv())

async def run_agent():
    AGENT_NAME = "stock_report_agent"
    AGENT_DESCRIPTION = "An agent that provides US stock prices and info."
    PORT = 10000
    HOST = "0.0.0.0"
    AGENT_URL = f"http://{HOST}:{PORT}"
    AGENT_VERSION = "1.0.0"
    MODEL = 'gemini-2.5-flash'
    AGENT_SKILLS = [
        AgentSkill(
            id="SKILL_STOCK_REPORT",
            name="stock_report",
            description="Provides stock prices and info.",
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

    stocks_tools, stocks_exit_stack = await return_sse_mcp_tools_stocks()

    stock_analysis_agent = ADKAgent(
        model=MODEL,
        name="stock_analysis_agent",
        description="Handles stock analysis and provides insights, in particular, can get the latest stock price.",
        tools=stocks_tools,
        instructions=(
            "Analyze stock data and provide insights. You can also get the latest stock price."
            "If the user asks about a company, the stock prices for the said company."
            "If the user asks about a stock, provide the latest stock price and any other relevant information."
            "You can get only the latest stock price for US companies."
        ),
    )

    task_manager = generate_agent_task_manager(
        agent=stock_analysis_agent,
    )
    server = A2AServer(
        host=HOST,
        port=PORT,
        endpoint="/stock_agent",
        agent_card=AGENT_CARD,
        task_manager=task_manager
    )
    print(f"Starting {AGENT_NAME} A2A Server on {AGENT_URL}")
    await server.astart()


if __name__ == "__main__":
    asyncio.run(
        run_agent()
    )
