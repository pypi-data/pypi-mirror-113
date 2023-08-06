from clisy.searcher.base_searcher import BaseSearcher


class CreativeCommonsImageSearcher(BaseSearcher):
    def __init__(self):
        super(CreativeCommonsImageSearcher, self).__init__("https://search.creativecommons.org/search/image?q=")

    def open(self, query_string):
        super(CreativeCommonsImageSearcher, self).open(query_string)
