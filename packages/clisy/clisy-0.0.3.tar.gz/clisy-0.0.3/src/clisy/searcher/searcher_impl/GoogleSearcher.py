from clisy.webview.web_browser_opener import WebBrowserOpener


class GoogleSearcher:
    query_url = "https://www.google.co.in/search?q="

    def open(self, query_string):
        WebBrowserOpener().open(self.query_url, query_string)
