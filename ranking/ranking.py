class PageRank:
    def __init__(self, indexer):
        self.indexer = indexer
        self.ranks = {}

    async def calculate_pagerank(self):
        num_documents = len(self.indexer.documents)
        if num_documents == 0:
            return

        teleport_probability = 0.85
        initial_rank = 1.0 / num_documents
        tolerance = 0.0001

        # Initialize ranks and dangling weights for each document
        self.ranks = {doc.url: initial_rank for doc in self.indexer.documents}
        dangling_weights = {doc: 0 for doc in self.indexer.documents}  # Proper initialization

        while True:
            new_ranks = {}
            total_dangling_weight = sum(self.ranks[doc.url] for doc in self.indexer.documents if len(doc.links) == 0)
            for document in self.indexer.documents:
                rank = (1 - teleport_probability) / num_documents
                rank += teleport_probability * total_dangling_weight / num_documents  # Distribute dangling weights
                for link in document.links:
                    if link.target.url in self.ranks:
                        rank += teleport_probability * self.ranks[link.target.url] / len(link.target.links)
                new_ranks[document.url] = rank

            # Check for convergence
            if all(abs(self.ranks[url] - new_ranks[url]) < tolerance for url in self.ranks):
                break

            self.ranks = new_ranks
    async def search(self, query):
        # Filter and sort documents based on the query presence in content and their rank
        query = query.lower()
        results = [(doc.url, self.ranks[doc.url], doc.title) for doc in self.indexer.documents if query in doc.content.lower()]
        results.sort(key=lambda x: x[1], reverse=True)  # Sort by rank
        return results
    
    print("PageRank Calculation Completed")