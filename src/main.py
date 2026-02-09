# template_scraping/src/main.py
import httpx
import asyncio
from selectolax.parser import HTMLParser
from helpers.utils import save_to_csv
from helpers.utils import gather_data
from loguru import logger

NUM_PAGES = 51


def parse_page(html):
    tree = HTMLParser(html)
    return gather_data(tree)


async def fetch_page(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return parse_page(response.text)
        else:
            return []


async def main():
    urls = [
        f"https://books.toscrape.com/catalogue/page-{i}.html"
        for i in range(1, NUM_PAGES)
    ]  # fill this with the urls

    # async with httpx.AsyncClient() as client:
    tasks = [fetch_page(url) for url in urls]
    logger.debug(f"Tasks: {len(tasks)}")
    results = await asyncio.gather(*tasks)

    results = [item for sublist in results for item in sublist]
    logger.debug(f"Results: {len(results)}")
    # results is a list of dictionaries
    save_to_csv(results)


asyncio.run(main())
