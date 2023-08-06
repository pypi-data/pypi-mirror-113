from clisy.searcher.base_searcher import BaseSearcher


class DuckDuckGoSearcher(BaseSearcher):
    def __init__(self):
        super(DuckDuckGoSearcher, self).__init__("https://duckduckgo.com/?q=")

    def open(self, query_string):
        super(DuckDuckGoSearcher, self).open(query_string)
