class UrlOrQuery:
    def __init__(self, url_or_query: str):
        import parse
        self.url_or_query = url_or_query
        self.format_strings = ["{}://{}/{}", "{}://{}/{}"]
        self.isUrl = True
        for fm_str in self.format_strings:
            try: result = list(parse.parse(fm_str, url_or_query))
            except TypeError: result = []
            if result != []: break
        if result == []:
            self.isUrl = False
        else:
            self.protocol = result[0]
            self.domain = result[1]
            self.other = result[2:]
        self.colors = ["green", "black", "gray"]

    def set_colors(self, protocol: str, domain: str, rest: str):
        self.colors = []
        self.colors.append(protocol)
        self.colors.append(domain)
        self.colors.append(rest)

    def __str__(self):
        if self.isUrl:
            return f"<span style='color: {self.colors[0]};'>{self.protocol}://</span><span style='color: {self.colors[1]};'>{self.domain}</span><span style='color: {self.colors[2]};'>/{'/'.join(self.other)}</span>"
        else:
            return self.url_or_query