import urllib.robotparser

# Defines the AsyncRobots class that uses urllib's RobotFileParser to check robots.txt rules.
class AsyncRobots:
    # Constructor: Initializes an AsyncRobots object with a base URL.
    def __init__(self, base_url):
        self.parser = urllib.robotparser.RobotFileParser()  # Creates an instance of RobotFileParser.
        self.parser.set_url(urllib.parse.urljoin(base_url, 'robots.txt'))  # Sets the URL of the robots.txt file based on the base URL.
        self.parser.read()  # Reads and parses the robots.txt file.

    # Asynchronous method to check if a specific user agent can fetch a URL according to the robots.txt rules.
    async def can_fetch(self, user_agent, url):
        return self.parser.can_fetch(user_agent, url)  # Returns True if fetching is allowed, False otherwise.
