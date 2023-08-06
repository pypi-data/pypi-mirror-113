from clisy.webview.web_browser_opener import WebBrowserOpener


class DuckDuckGoSearcher:
    duck_duck_go_query_url = "https://duckduckgo.com/?q="

    def open(self, query_string):
        WebBrowserOpener().open(self.duck_duck_go_query_url + query_string)
