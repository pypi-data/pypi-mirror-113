from clisy.searcher.base_searcher import BaseSearcher


class WikipediaSearcher(BaseSearcher):
    def __init__(self):
        super(WikipediaSearcher, self).__init__("https://en.wikipedia.org/w/index.php?search=")

    def open(self, query_string):
        super(WikipediaSearcher, self).open(query_string)
