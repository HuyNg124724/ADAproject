import asyncio
import urllib.parse
import aiohttp
from bs4 import BeautifulSoup
from indexer.models import Document
from crawler.async_robots import AsyncRobots

class Crawler:
    # Constructor: Initializes the crawler with a start URL, maximum depth for crawling, and sets up containers for URLs and documents.
    def __init__(self, start_url, max_depth=3):
        self.start_url = start_url   # The URL where crawling starts
        self.max_depth = max_depth   # Maximum depth to crawl
        self.visited_urls = set()    # Set to store visited URLs to avoid revisiting
        self.documents = []          # List to store the documents fetched

    # Asynchronous fetch method to handle HTTP requests and parse responses
    async def fetch(self, url, session, robots, depth):
        if url in self.visited_urls or depth > self.max_depth:
            return None  # Skip if the URL has already been visited or depth limit exceeded
        self.visited_urls.add(url)  # Mark the URL as visited
        
        try:
            async with session.get(url) as response:  # Asynchronously send a GET request to the URL
                if response.status == 200 and await robots.can_fetch("MyBot", url):  # Check if request is successful and allowed by robots.txt
                    content = await response.text()  # Read the response content as text
                    soup = BeautifulSoup(content, 'html.parser')  # Parse the HTML content with BeautifulSoup
                    title = soup.title.string if soup.title else url  # Extract the title or use URL if title absent
                    document = Document(url, title, content)  # Create a Document object
                    self.documents.append(document)  # Add the document to the list

                    if depth < self.max_depth:
                        links = self.get_links(soup, url)  # Extract links from the page
                        tasks = [self.fetch(link, session, robots, depth + 1) for link in links]  # Create sub-tasks for each link
                        await asyncio.gather(*tasks)  # Asynchronously gather all sub-tasks
                    return document
        except Exception as e:
            print(f"Error fetching {url}: {e}")  # Print any errors encountered during fetch
        return None

    # Method to extract all hyperlinks from a BeautifulSoup parsed HTML and return as a set of absolute URLs
    def get_links(self, soup, base_url):
        links = set()  # Set to store absolute URLs
        for link in soup.find_all('a', href=True):  # Find all anchor tags with href attribute
            href = link['href']
            full_url = urllib.parse.urljoin(base_url, href)  # Convert relative URL to absolute URL
            if full_url not in self.visited_urls:
                links.add(full_url)  # Add to the set if not already visited
        return links

    # Main crawl method to start the crawling process
    async def crawl(self):
        async with aiohttp.ClientSession() as session:  # Open an asynchronous HTTP session
            robots = AsyncRobots(self.start_url)  # Create an instance of AsyncRobots to handle robots.txt
            await self.fetch(self.start_url, session, robots, depth=1)  # Start fetching from the initial URL

