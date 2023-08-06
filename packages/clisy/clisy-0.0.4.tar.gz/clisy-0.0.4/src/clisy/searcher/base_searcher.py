from clisy.webview.web_browser_opener import WebBrowserOpener


class BaseSearcher:
    query_url = ""

    def __init__(self, query_url):
        self.query_url = query_url

    def open(self, query_string):
        WebBrowserOpener().open(self.query_url, query_string)
