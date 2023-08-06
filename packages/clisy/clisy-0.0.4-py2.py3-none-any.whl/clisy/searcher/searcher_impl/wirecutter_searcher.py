from clisy.searcher.base_searcher import BaseSearcher


class WirecutterSearcher(BaseSearcher):
    def __init__(self):
        super(WirecutterSearcher, self).__init__("https://www.nytimes.com/wirecutter/search/?s=")

    def open(self, query_string):
        super(WirecutterSearcher, self).open(query_string)
