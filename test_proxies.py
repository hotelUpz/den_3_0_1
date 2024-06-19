import requests

proxy_host = '109.122.60.50'
proxy_port = '50100'
proxy_socks5_port = '50101'
proxy_username = 'nikolassmsttt'
proxy_password = 'pRcwSxcJtT'

proxy_url = f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'
proxy_soks5_url = f'soks5://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_socks5_port}'

proxies = {
    # 'http': proxy_url,
    # 'https': proxy_url,
    "socks5": proxy_soks5_url
}

try:
    response = requests.get('http://example.com', proxies=proxies)
    print(response.text)
except Exception as e:
    print(f'Error occurred: {e}')

import requests
from bs4 import BeautifulSoup
get_location_link = 'https://2ip.ru'


def checkIP(): 

    proxiess = {
        # "https": proxy_url,
        # "http": proxy_url,
        "socks5": proxy_soks5_url

    }
    try:
        response = requests.get(url=get_location_link, proxies=proxiess)
        soup = BeautifulSoup(response.text, 'lxml')
        ip = soup.find('div', class_ = 'ip').text.strip()
        location = soup.find('div', class_ = 'value-country').text.strip()
        print(ip, ':', location)
    
    except Exception as ex:
        print(ex)
     

checkIP()
