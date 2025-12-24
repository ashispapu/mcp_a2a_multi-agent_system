import asyncio

from dotenv import load_dotenv, find_dotenv
from google.adk import Agent, Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.genai import types

from adk_agents_testing.mcp_tools.mcp_tool_search import return_sse_mcp_tools_search
from adk_agents_testing.mcp_tools.mcp_tool_stocks import return_sse_mcp_tools_stocks

from termcolor import colored

load_dotenv(find_dotenv())

MODEL = 'gemini-2.5-pro-exp-03-25'
APP_NAME = 'company_analysis_app'
USER_ID = 'searcher_usr'
SESSION_ID = 'searcher_session'

async def async_main():
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()
    print(colored(text="Creating session...", color='blue'))
    session = session_service.create_session(
        state={},
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    print(colored(text="Session created!", color='blue'))

    query = input("Enter your query:\n")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    search_tools, search_exit_stack = await return_sse_mcp_tools_search()
    stocks_tools, stocks_exit_stack = await return_sse_mcp_tools_stocks()


    stock_analysis_agent = Agent(
        model=MODEL,
        name="stock_analysis_agent",
        instruction="Analyze stock data and provide insights.",
        description="Handles stock analysis and provides insights, in particular, can get the latest stock price.",
        tools=stocks_tools,
    )
    search_agent = Agent(
        model=MODEL,
        name="search_agent",
        instruction="Expert googler. Can search anything on google and read pages online.",
        description="Handles search queries and can read pages online.",
        tools=search_tools,
    )

    root_agent = Agent(
        name="company_analysis_assistant",
        model=MODEL,
        description="Main assistant: Handles requests about stocks and information of companies.",
        instruction=(
            "You are the main Assistant coordinating a team. Your primary responsibilities are providing company and stocks reports and delegating other tasks.\n"
            "1. If the user asks about a company, provide a detailed report.\n"
            "2. If you need any information about the current stock price, delegate to the stock_analysis_agent.\n"
            "3. If you need to search for information, delegate to the search_agent.\n"
            "Analyze the user's query and delegate or handle it appropriately. If unsure, ask for clarification. Only use tools or delegate as described."
        ),
        sub_agents=[search_agent, stock_analysis_agent],
        output_key="last_assistant_response",
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    print(colored(text="Running agent...", color='blue'))
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            print(colored(text=f"############# Final Response #############\n\n{final_response_text}", color='green'))
            break
        else:
            print(event)


    print("Closing MCP server connection...")
    await stocks_exit_stack.aclose()
    await search_exit_stack.aclose()
    print("Cleanup complete.")


if __name__ == '__main__':
    asyncio.run(async_main())
