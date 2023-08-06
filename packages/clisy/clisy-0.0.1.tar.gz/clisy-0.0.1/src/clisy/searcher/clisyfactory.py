import logging

from src.clisy.searcher.searcher_impl.duck_duck_go_searcher import DuckDuckGoSearcher
from src.clisy.searcher.searchoptions import SearchOptions


class ClisyFactory:
    _logger = logging.getLogger(__name__)
    searchers = {
        SearchOptions.DUCKDUCKGO: DuckDuckGoSearcher
    }

    def __init__(self):
        self.search_option = SearchOptions.DUCKDUCKGO

    def __init__(self, search_option):
        self.search_option = search_option

    def get_searcher(self):
        try:
            return self.searchers[self.search_option]()
        except Exception as ex:
            self._logger.error(self,
                               "This search is not yet supported. Please refer to documentation to understand what "
                               "all options are supported at present. Following are the search options supported so "
                               "far : %s . Here is the error %r",
                               SearchOptions, ex)
