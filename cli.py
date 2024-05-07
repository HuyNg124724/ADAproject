import sys
import asyncio
from crawler.crawler import Crawler
from indexer.indexer import Indexer
from ranking.ranking import PageRank

# Main asynchronous function to execute the web crawling, indexing, and ranking based on the provided URL and query.
async def main(start_url, query):
    crawler = Crawler(start_url)  # Initialize the Crawler with a start URL.
    await crawler.crawl()  # Perform the crawl operation asynchronously.

    indexer = Indexer()  # Initialize the Indexer.
    await indexer.add_documents(crawler.documents)  # Add the crawled documents to the indexer.

    pagerank = PageRank(indexer)  # Initialize the PageRank calculator with the indexer.
    await pagerank.calculate_pagerank()  # Calculate the PageRank for the indexed documents.

    # Handle search query if provided
    if query:
        print("Search Results:")
        results = await pagerank.search(query)  # Perform a search based on the query.
        if results:
            # If results are found, format and print them
            print("+-------------------------------------------------------------------------------------------------------+")
            print("| Title                                     | URL                                                     | Rank    |")
            print("+-------------------------------------------------------------------------------------------------------+")
            for url, rank, title in results:
                print(f"| {title.ljust(40)} | {url.ljust(50)} | {rank:.4f} |")
            print("+-------------------------------------------------------------------------------------------------------+")
        else:
            print("No results found for the query.")
    else:
        print("No query provided.")

# Entry point of the script
if __name__ == "__main__":
    # Check if the required arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python cli.py <start_url> [query]")  # Inform the user how to run the script
        sys.exit(1)  # Exit if not enough arguments are provided
    start_url = sys.argv[1]  # The first argument is the start URL
    query = sys.argv[2] if len(sys.argv) > 2 else ''  # The second argument is the optional query
    asyncio.run(main(start_url, query))  # Run the main function with asyncio
