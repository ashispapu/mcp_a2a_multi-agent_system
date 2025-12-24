import os
from typing import Dict, Any

import finnhub
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class FinHubService:
    def __init__(self):
        """
        Initialises the finhubservice.
        """
        self.client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

    def get_symbol_from_query(self, query: str) -> Dict[str,Any]:
        """
        Given a query (e.g. name of a company) returns a dictionary with info. Use only if you have no idea about the symbol.
        :param query: name of company
        :return: dictionary with the response to the query
        """

        return self.client.symbol_lookup(
            query=query,
        )

    def get_price_of_stock(self, symbol: str) -> Dict[str,Any]:
        """
        Given the symbol of a certain strock, returns the live info about it.
        :param symbol: The symbol of a stock, e.g. AAPL
        :return: a dictionary containing the current_price, change, %change, day high, low, opening and previous closing price
        """
        resp = self.client.quote(symbol)
        return {
             'current_price': resp['c'],
             'change': resp['d'],
             'percentage_change': resp['dp'],
             'day_high': resp['h'],
             'day_low': resp['l'],
             'day_open_price': resp['o'],
             'previous_close_price': resp['pc'],
         }

if __name__ == "__main__":
    service = FinHubService()
    print(service.get_symbol_from_query("Tinexta"))
    print(service.get_price_of_stock("AAPL"))