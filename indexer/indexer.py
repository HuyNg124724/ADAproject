# Import statements to include necessary classes from the models module
from .models import Document, Link

# Definition of the Indexer class
class Indexer:
    # Constructor of the Indexer class
    def __init__(self):
        self.documents = []  # Initializes an empty list to store documents
        self.links = []      # Initializes an empty list to store links between documents

    # Asynchronous method to add multiple documents to the indexer
    async def add_documents(self, documents):
        for document in documents:
            self.add_document(document)  # Calls the add_document method for each document

    # Method to add a single document to the indexer's list of documents
    def add_document(self, document):
        self.documents.append(document)  # Appends the document to the documents list

    # Method to add a link between two documents
    def add_link(self, source, target):
        link = Link(source, target)  # Creates a new Link object with source and target documents
        self.links.append(link)      # Appends the new link to the links list
