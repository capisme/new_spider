DEFAULT_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}


class NewsRequest:
    def __init__(self, url, method='get', headers=DEFAULT_HEADERS,
                 data=None, json=None, verify=True, proxy=None,
                 timeout=8,
                 allow_redirects=True,
                 callback=None,
                 meta={},
                 priority=100,
                 request_type=0  # 0代表普通请求 1 代表 chrom请求
                 ):
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data
        self.json = json
        self.verify = verify
        self.proxy = proxy
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.callback = callback
        self.meta = meta
        self.priority = priority
        self.request_type = request_type
