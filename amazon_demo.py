import time,re
import requests
import ssl
import requests

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context

# see "openssl ciphers" command for cipher names
CIPHERS = "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384"


class TlsAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)



if __name__ == "__main__":
    
    keyword = 'iphone'
    site_home_url = 'https://www.amazon.co.uk'
    start_url = 'https://www.amazon.co.uk/s?k='+keyword
    
    adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    session = requests.session()
    session.mount("https://", adapter)
    
    headers =  {
        "authority" : "www.amazon.co.uk",
        "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language" : "zh-CN,zh;q=0.9",
        "sec-ch-ua" : '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "sec-ch-ua-mobile" : "?0",
        "sec-ch-ua-platform" : '"Windows"',
        "sec-fetch-dest" : "document",
        "sec-fetch-mode" : "navigate",
        "sec-fetch-site" : "none",
        "sec-fetch-user" : "?1",
        "upgrade-insecure-requests" : "1",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }  
    res = session.get(start_url, headers=headers)
    html = res.text.encode('utf-8')
    
    search_items = re.findall('<a class="a-link-normal s-no-outline" href="([^\"]*)">', html.decode('utf-8'))
    search_items_array = []
    if search_items:
        target_item_url = site_home_url+search_items[0]
        res =  session.get(target_item_url, headers=headers)
        html = res.text.encode('utf-8')
        print(html)
