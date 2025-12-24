from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseServerParams
from mcp import StdioServerParameters


async def return_mcp_tools_stocks():
    print("Attempting to connect to MCP server for stocks analyis read...")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="/opt/homebrew/bin/uv",
            args=[
                "--directory",
                "/Users/tsadoq/gits/a2a-mcp-tutorial/mcp_server",
                "run",
                "stocks_server.py"
            ],
            env={
                "MCP_PORT":"8001",
                "PYTHONPATH": "/Users/tsadoq/gits/a2a-mcp-tutorial:${PYTHONPATH}"
            },
        )
    )
    print("MCP Toolset created successfully.")
    return tools, exit_stack

async def return_sse_mcp_tools_stocks():
    print("Attempting to connect to MCP server for stock info...")
    server_params = SseServerParams(
        url="http://localhost:8181/sse",
    )
    tools, exit_stack = await MCPToolset.from_server(connection_params=server_params)
    print("MCP Toolset created successfully.")
    return tools, exit_stack