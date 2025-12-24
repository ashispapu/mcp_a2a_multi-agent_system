from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseServerParams
from mcp import StdioServerParameters


async def return_mcp_tools_search():
    print("Attempting to connect to MCP server for search and page read...")
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
                "MCP_PORT":"8000",
                "PYTHONPATH": "/Users/tsadoq/gits/a2a-mcp-tutorial:${PYTHONPATH}"
            },
        )
    )
    print("MCP Toolset created successfully.")
    return tools, exit_stack


async def return_sse_mcp_tools_search():
    print("Attempting to connect to MCP server for search and page read...")
    server_params = SseServerParams(
        url="http://localhost:8080/sse",
    )
    tools, exit_stack = await MCPToolset.from_server(connection_params=server_params)
    print("MCP Toolset created successfully.")
    return tools, exit_stack
