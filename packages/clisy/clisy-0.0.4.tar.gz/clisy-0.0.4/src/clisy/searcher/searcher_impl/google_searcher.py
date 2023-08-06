from clisy.searcher.base_searcher import BaseSearcher


class GoogleSearcher(BaseSearcher):
    def __init__(self):
        super(GoogleSearcher, self).__init__("https://www.google.co.in/search?q=")

    def open(self, query_string):
        super(GoogleSearcher, self).open(query_string)
