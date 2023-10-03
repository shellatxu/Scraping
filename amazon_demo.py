import re
import requests
import ssl
from bs4 import BeautifulSoup
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

def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
        
    for select in form.find_all("select"):
        # get the name attribute
        select_name = select.attrs.get("name")
        # set the type as select
        select_type = "select"
        select_options = []
        # the default select value
        select_default_value = ""
        # iterate over options and get the value of each
        for select_option in select.find_all("option"):
            # get the option value used to submit the form
            option_value = select_option.attrs.get("value")
            if option_value:
                select_options.append(option_value)
                if select_option.attrs.get("selected"):
                    # if 'selected' attribute is set, set this option as default    
                    select_default_value = option_value
        if not select_default_value and select_options:
            # if the default is not set, and there are options, take the first option as default
            select_default_value = select_options[0]
        # add the select to the inputs list
        inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})
    for textarea in form.find_all("textarea"):
        # get the name attribute
        textarea_name = textarea.attrs.get("name")
        # set the type as textarea
        textarea_type = "textarea"
        # get the textarea value
        textarea_value = textarea.attrs.get("value", "")
        # add the textarea to the inputs list
        inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

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
    
    # find product list items
    search_items = re.findall('<a class="a-link-normal s-no-outline" href="([^\"]*)">', html.decode('utf-8'))
    search_items_array = []
    if search_items:
        # just get the first product
        target_item_url = site_home_url+search_items[0]
        res =  session.get(target_item_url, headers=headers)
        html = res.text.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        
        # get the add to cart form
        all_forms = soup.find_all("form")

        fd = get_form_details(all_forms[2])

        add_cart_url = site_home_url+fd['action']
        
        data = {}
        
        for input_tag in fd["inputs"]:
            if input_tag["type"] == "hidden":
                data[input_tag["name"]] = input_tag["value"]
            elif input_tag["type"] == "select":
                for i, option in enumerate(input_tag["values"], start=1):
                    if option == input_tag["value"]:
                        print(f"{i} # {option} (default)")
                    else:
                        print(f"{i} # {option}")
                choice = input(f"Enter the option for the select field '{input_tag['name']}' (1-{i}): ")
                try:
                    choice = int(choice)
                except:
                    value = input_tag["value"]
                else:
                    value = input_tag["values"][choice-1]
                data[input_tag["name"]] = value
            elif input_tag["type"] != "submit":
                value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
                data[input_tag["name"]] = value        

        # submit add cart form 
        res = session.post(add_cart_url, data=data, headers=headers)
        html = res.text.encode('utf-8')

        # get the cart items number
        cart_item_count = re.findall('<span id="nav-cart-count" aria-hidden="true" class="nav-cart-count nav-cart-1 nav-progressive-attribute nav-progressive-content">([\d]*)</span>', html.decode('utf-8'))
        print(cart_item_count)
        
        
