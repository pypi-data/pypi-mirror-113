from clisy.webview.web_browser_opener import WebBrowserOpener


class DuckDuckGoSearcher:
    query_url = "https://duckduckgo.com/?q="

    def open(self, query_string):
        WebBrowserOpener().open(self.query_url, query_string)
