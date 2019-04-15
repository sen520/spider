import requests


class HtmlDownload(object):
    def download(self, url):
        if url is None:
            return
        s = requests.Session()
        s.headers[
            'User-Agent'] = 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 63.0.3239.132Safari / 537.36'
        res = s.get(url)

        if res.status_code == 200:
            res.encoding = 'utf-8'
            res = res.text
            return res
        return None

