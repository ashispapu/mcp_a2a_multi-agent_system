import asyncio
import os

from google.adk import Runner
from google.genai import types
from dotenv import load_dotenv, find_dotenv
from google.adk.agents import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool import MCPToolset
from mcp import StdioServerParameters

load_dotenv(find_dotenv())

async def get_tools_async():
  """Gets tools from the Search MCP Server."""
  print("Attempting to connect to MCP Filesystem server...")
  tools, exit_stack = await MCPToolset.from_server(
      connection_params=StdioServerParameters(
          command="/opt/homebrew/bin/uv",
          args=[
              "--directory",
              "/Users/tsadoq/gits/a2a-mcp-tutorial/mcp_server",
              "run",
              "search_server.py"
          ],
          env={
              "PYTHONPATH": "/Users/tsadoq/gits/a2a-mcp-tutorial:${PYTHONPATH}"
          },
      )
  )
  print("MCP Toolset created successfully.")
  return tools, exit_stack

async def get_agent_async():
  """Creates an ADK Agent equipped with tools from the MCP Server."""
  tools, exit_stack = await get_tools_async()
  print(f"Fetched {len(tools)} tools from MCP server.")
  root_agent = LlmAgent(
      model='gemini-2.5-pro-exp-03-25', # Adjust model name if needed based on availability
      name='search_agent',
      description="Agent to answer questions using Google Search.",
      instruction="You are an expert researcher. When someone asks you something you always double check online. You always stick to the facts.",
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return root_agent, exit_stack

async def async_main():
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()
    print("Creating session...")
    session = session_service.create_session(
        state={}, app_name='mcp_search_app', user_id='searcher_usr', session_id='searcher_session'
    )
    print(f"Session created with ID: {session.id}")

    query = "Quali sono gli sport tipici della valle d'aosta? Rispondi in maniera precisa e piena di dettagli"
    print(f"User Query: '{query}'")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    root_agent, exit_stack = await get_agent_async()

    runner = Runner(
        app_name='mcp_search_app',
        agent=root_agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            print(f"############# Final Response #############\n\n{final_response_text}")
            break


    print("Closing MCP server connection...")
    await exit_stack.aclose()
    print("Cleanup complete.")


if __name__ == '__main__':
    asyncio.run(async_main())
