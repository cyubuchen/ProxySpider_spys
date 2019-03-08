import os
import re
import time
import random
import threading
from multiprocessing import Pool
import requests
from requests.exceptions import ProxyError, ConnectionError, ReadTimeout, Timeout
from proxy_config import *


unchecked = []
file_path_checked = '{0}/{1}.txt'.format(os.getcwd(), CHECKED_PROXY)

# GET HTML [Per page|ANM|SSL|Port|Type]
def get_index(xpp, xf1, xf2, xf4, xf5):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'}
    data = {
        'xpp': xpp,
        'xf1': xf1,
        'xf2': xf2,
        'xf4': xf4,
        'xf5': xf5
    }
    print('Getting the website...')
    try:
        rsp = requests.post(url=url, headers=header, data=data)
        if rsp.status_code == 200:
            print('Success.')
            html = rsp.text
            return html
        else:
            exit('Can not get the website.')
    except requests.exceptions.ConnectionError:
        exit('Please run your proxy app and try again.')

def get_proxy_info(html):
    pattern = re.compile('onmouseout.*?spy14>(.*?)<s.*?write.*?nt>\"\+(.*?)\)</scr.*?\/en\/(.*?)-', re.S)
    infos = re.findall(pattern, html)
    return infos

def parse_proxy_info(html, infos):
    print('Get {} proxies.'.format(len(infos)))
    print('Start to get proxy details...')
    port_word = re.findall('\+\(([a-z0-9^]+)\)+', html)
    # DECRYPT PORT VALUE
    port_passwd = {}
    portcode = (re.findall('table><script type="text/javascript">(.*)</script>', html))[0].split(';')
    for i in portcode:
        ii = re.findall('\w+=\d+', i)
        for i in ii:
            kv = i.split('=')
            if len(kv[1]) == 1:
                k = kv[0]
                v = kv[1]
                port_passwd[k] = v
            else:
                pass
    # GET PROXY INFO
    for i in infos:
        proxies_info = {
            'ip': i[0],
            'port': i[1],
            'protocol': i[2]
        }
        port_word = re.findall('\((\w+)\^', proxies_info.get('port'))
        port_digital = ''
        for i in port_word:
            port_digital += port_passwd[i]
        test_it = '{0}://{1}:{2}'.format(proxies_info.get('protocol'), proxies_info.get('ip'), port_digital)
        if 'socks' in test_it:
            test_it = '{0}5://{1}:{2}'.format(proxies_info.get('protocol'), proxies_info.get('ip'), port_digital)
        else:
            test_it = '{0}://{1}:{2}'.format(proxies_info.get('protocol'), proxies_info.get('ip'), port_digital)
        unchecked.append(test_it)

def ckeck_proxy(list_part):
    for proxy in list_part:
        threading.Thread(target=thread_check, args=(proxy, )).start()

def thread_check(proxy):
    url_test = 'http://checkip.org/'
    url_tests = 'https://checkip.org/'
    headers = {'User-Agent': ''}
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000'
    ]
    headers['User-Agent'] = random.choice(user_agent_list)
    try:
        if 's' in proxy:
            proxy_ = {'https': proxy}
            rsp = requests.get(url_tests, headers=headers, proxies=proxy_, timeout=5)
        else:
            proxy_ = {'http': proxy}
            rsp = requests.get(url_test, headers=headers, proxies=proxy_, timeout=5)
        if rsp.status_code == 200:
            with open(file_path_checked, 'a+') as f:
                ip_pattern = re.compile('Your IP Address.*?>(.*?)<.*?Country:(.*?)<.*?ISP:(.*?)<', re.S)
                ip_check = re.findall(ip_pattern, rsp.text)
                print('CHECKING: {0} --> WORKING {1} Save to: {2}\n'.format(ip_check[0][0], proxy, file_path_checked))
                f.write('{0} | {1} | {2} | {3}\n'.format(format(proxy, '<30'),format(rsp.elapsed.total_seconds(), '<15'), format(ip_check[0][1], '<20'), ip_check[0][2]))
        else:
            print('NOT WORKING: {0}\n'.format(proxy))
    except (ProxyError, ConnectionError, ReadTimeout, Timeout):
        print('BAD PROXY: {0}\n'.format(proxy))
    except:
        pass

def main():
    html = get_index(xpp, xf1, xf2, xf4, xf5)
    infos = get_proxy_info(html)
    parse_proxy_info(html, infos)
    with open(file_path_checked,'w') as f:
        f.write('{0} | {1} | {2} | {3}\n'.format(format('Proxy', '<30'), format('Responese Time', '<15'), format('Region', '<20'), 'ISP'))
    p = Pool(10)
    list_part = [unchecked[i:i+50] for i in range(0, len(unchecked), 50)]
    print('Checking proxy...')
    start_time = time.time()
    for i in range(10):
        p.apply_async(ckeck_proxy, (list_part[i], ))
    p.close()
    p.join()
    print('Check proxies takes {0:.2f}s.\nDONE.'.format(time.time() - start_time))

if __name__ == '__main__':
    main()