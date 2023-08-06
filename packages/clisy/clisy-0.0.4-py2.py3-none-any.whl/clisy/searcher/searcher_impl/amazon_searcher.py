from clisy.searcher.base_searcher import BaseSearcher


class AmazonSearcher(BaseSearcher):
    def __init__(self):
        super(AmazonSearcher, self).__init__("https://www.amazon.in/s?k=")

    def open(self, query_string):
        super(AmazonSearcher, self).open(query_string)
