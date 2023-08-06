from clisy.searcher.base_searcher import BaseSearcher


class IMDbSearcher(BaseSearcher):
    def __init__(self):
        super(IMDbSearcher, self).__init__("https://www.imdb.com/find?q=")

    def open(self, query_string):
        super(IMDbSearcher, self).open(query_string)
