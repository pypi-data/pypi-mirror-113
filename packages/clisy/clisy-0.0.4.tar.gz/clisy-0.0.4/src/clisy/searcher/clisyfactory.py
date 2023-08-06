import logging

from clisy.searcher.searcher_impl.amazon_searcher import AmazonSearcher
from clisy.searcher.searcher_impl.creative_commons_image_searcher import CreativeCommonsImageSearcher
from clisy.searcher.searcher_impl.duck_duck_go_searcher import DuckDuckGoSearcher
from clisy.searcher.searcher_impl.google_searcher import GoogleSearcher
from clisy.searcher.searcher_impl.imdb_searcher import IMDbSearcher
from clisy.searcher.searcher_impl.swiggy_searcher import SwiggySearcher
from clisy.searcher.searcher_impl.wikipedia_searcher import WikipediaSearcher
from clisy.searcher.searcher_impl.wirecutter_searcher import WirecutterSearcher
from clisy.searcher.searchoptions import SearchOptions


class ClisyFactory:
    _logger = logging.getLogger(__name__)
    searchers = {
        SearchOptions.DUCKDUCKGO: DuckDuckGoSearcher,
        SearchOptions.GOOGLE: GoogleSearcher,
        SearchOptions.WIKIPEDIA: WikipediaSearcher,
        SearchOptions.WIRECUTTER: WirecutterSearcher,
        SearchOptions.AMAZON: AmazonSearcher,
        SearchOptions.CREATIVE_COMMONS_IMAGE: CreativeCommonsImageSearcher,
        SearchOptions.IMDB: IMDbSearcher,
        SearchOptions.SWIGGY: SwiggySearcher
    }

    def __init__(self):
        self.search_option = SearchOptions.DUCKDUCKGO

    def __init__(self, search_option=str):
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
