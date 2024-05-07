class Document:
    def __init__(self, url, title, content):
        self.url = url          # URL of the document, acts as a unique identifier.
        self.title = title      # Title of the document.
        self.content = content  # Content of the document, which could be text, HTML, or any other format.
        self.links = []         # A list to store links to other documents.

    def add_link(self, link):
        self.links.append(link)  # Adds a link to the list of links.


class Link:
    def __init__(self, source_document, target_document):
        self.source = source_document  # The document from which the link originates.
        self.target = target_document  # The document to which the link points.
        