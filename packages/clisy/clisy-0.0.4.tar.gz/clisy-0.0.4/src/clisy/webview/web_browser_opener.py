import logging
import subprocess
from urllib.parse import quote_plus


class WebBrowserOpener:
    _logging = logging.getLogger(__name__)
    SYS_COMMAND_OPEN = "open"

    def open(self, query_url, query_string):
        if query_string:
            subprocess.call([self.SYS_COMMAND_OPEN, query_url + quote_plus(query_string)])
        else:
            self._logging.error("Please provide query string to search for")
