import json
import os
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class SerperDevService:
    def __init__(self):
        self.__api_key__=os.getenv("SERPER_DEV_API_KEY")
        self.search_url = "https://google.serper.dev/search"
        self.scraper_url = "https://scrape.serper.dev"

    def search_google(
            self,
            query: str,
            n_results: int = 10,
            page: int = 1,
    ) -> List[Dict[str, Any]]:
        """
        Search Google using the Serper.dev API.
        :param query: the query to search on google
        :param n_results: number of results to return per page
        :param page: page number to return
        :return: a list of dictionaries containing the search results
        """
        payload = json.dumps(
            {
                "q": query,
                "num": n_results,
                "page": page
            },
        )
        headers = {
            'X-API-KEY': self.__api_key__,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            method="POST",
            url=self.search_url,
            headers=headers,
            data=payload,
        )

        return response.json()['organic']


    def get_text_from_page(self, url_to_scrape: str) -> str:
        """
        Get text from a page using the Serper.dev API.
        :param url_to_scrape: the url of the page to scrape
        :return: the text content of the page
        """
        payload = json.dumps(
            {
                "url": url_to_scrape,
            }
        )
        headers = {
            'X-API-KEY': self.__api_key__,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            method="POST",
            url=self.scraper_url,
            headers=headers,
            data=payload,
        )

        return response.text
