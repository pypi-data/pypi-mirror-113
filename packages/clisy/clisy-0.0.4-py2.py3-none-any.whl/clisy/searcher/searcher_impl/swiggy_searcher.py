from clisy.searcher.base_searcher import BaseSearcher


class SwiggySearcher(BaseSearcher):
    def __init__(self):
        super(SwiggySearcher, self).__init__("https://www.swiggy.com/search?q=")

    def open(self, query_string):
        super(SwiggySearcher, self).open(query_string)
