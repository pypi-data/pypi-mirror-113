class SearchOptions:
    DUCKDUCKGO = "ddg"
    GOOGLE = "g"
    WIKIPEDIA = "w"
    WIRECUTTER = "wc"
    AMAZON = "a"
    CREATIVE_COMMONS = "cc"
    IMDB = "imdb"

    def __str__(self):
        return self.DUCKDUCKGO + "\n" \
               + self.GOOGLE + "\n" \
               + self.WIKIPEDIA + "\n" \
               + self.WIRECUTTER + "\n" \
               + self.AMAZON + "\n" \
               + self.CREATIVE_COMMONS + "\n" \
               + self.IMDB


if __name__ == "__main__":
    print(SearchOptions())
