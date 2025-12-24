import sys
import os
import uvicorn
from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from services.stocks_service.finhub_service import FinHubService

mcp = FastMCP("Stock Information Server")

search_service = FinHubService()

@mcp.tool()
def get_symbol_from_query(query: str) -> dict:
    """
    Get the symbol of a stock from a query using the FinHub API.
    :param query: the query to search for
    :return: a dictionary containing the symbol of the stock
    """
    return search_service.get_symbol_from_query(query)

@mcp.tool()
def get_price_of_stock(symbol: str) -> dict:
    """
    Get the price of a stock using the FinHub API.
    :param symbol: the symbol of the stock
    :return: a dictionary containing the price of the stock
    """
    return search_service.get_price_of_stock(symbol)


def create_starlette_app(
        mcp_server: Server,
        *,
        debug: bool = False,
) -> Starlette:
    """
    Create a Starlette application that can server the provied mcp server with SSE.
    :param mcp_server: the mcp server to serve
    :param debug: whether to enable debug mode
    :return: a Starlette application
    """

    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


if __name__ == "__main__":
    mcp_server = mcp._mcp_server  # noqa: WPS437

    import argparse

    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8181, help='Port to listen on')
    args = parser.parse_args()

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host=args.host, port=args.port)

