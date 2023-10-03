from .scrape import scraper
import asyncio

asyncio.run(scraper("United States", "Information", "Sales"))