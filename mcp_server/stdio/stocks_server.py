import sys
import os
from mcp.server.fastmcp import FastMCP

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
