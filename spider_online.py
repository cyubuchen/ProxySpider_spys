import os
import re
import time
import random
import threading
from multiprocessing import Pool
import requests
from requests.exceptions import ConnectionError


# ==================================================================== #

# Proxy file name
CHECKED_PROXY = 'checked_proxy'

url = 'http://spys.one/en/socks-proxy-list/'

# ==================================================================== #


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
	try:
		rsp = requests.post(url=url, headers=header, data=data)
		if rsp.status_code == 200:
			html = rsp.text
			return html
		else:
			exit('Can not get the website.')
	except ConnectionError:
		exit('Please run your proxy app and try again.')


def get_proxy_info(html):
	pattern = re.compile('onmouseout.*?spy14>(.*?)<.*?>"(.*?)<\/.*?>([HTTPS|SOCKS5]+)', re.S)
	info = re.findall(pattern, html)
	return info


def parse_proxy_info(html, info):
	if len(info) > 30:
		print('PROXY: {}'.format(len(info)))
	else:
		exit('Operation too frequent, please change your proxy and try again later.')
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
	for i in info:
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
		unchecked.append(test_it)


def ckeck_proxy(list_part):
	for proxy in list_part:
		threading.Thread(target=thread_check, args=(proxy, )).start()


def thread_check(proxy):
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
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000',
		"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", 
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)", 
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", 
		"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)", 
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)", 
		"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)", 
		"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)", 
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)", 
		"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6", 
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1", 
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0", 
		"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5", 
		"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6", 
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11", 
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20", 
		"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
	]
	headers['User-Agent'] = random.choice(user_agent_list)
	proxy_ = {'http': proxy, 'https': proxy}
	url_test = 'http://ip-api.com/json/'
	try:
		rsp = requests.get(url_test, headers=headers, proxies=proxy_, timeout=5)
		if rsp.status_code == 200:
			result = rsp.json()
			details = result['country'] + ' ' + result['city'] + ' ' + result['isp']
			with open(file_path_checked, 'a+') as f:
				f.write('{0} | {1} | {2}\n'.format(format(proxy, '<30'), format('{0:.2f}'.format(rsp.elapsed.total_seconds()), '<15'), format(details, '<20')))
				print('CHECKING: {} -> WORKING {} -> SAVE TO: {}\n'.format(proxy, result['query'], file_path_checked))
		else:
			print(f'NOT WORKING, {rsp.status_code}, {proxy}\n')
	except:
		print('BAD PROXY, {0}\n'.format(proxy))


def main():
	html = get_index(5, 0, 0, 0, 2)
	info = get_proxy_info(html)
	parse_proxy_info(html, info)
	with open(file_path_checked,'w') as f:
		f.write('{0} | {1} |  {2}\n'.format(format('Proxy', '<30'), format('Response Time', '<15'), format('ISP', '<19')))
	p = Pool(10)
	list_part = [unchecked[i:i+50] for i in range(0, len(unchecked), 50)]
	print('Checking...')
	start_time = time.time()
	for i in range(10):
		p.apply_async(ckeck_proxy, (list_part[i], ))
	p.close()
	p.join()
	print('Check proxies takes {0:.2f}s.\nDONE.'.format(time.time() - start_time))


if __name__ == '__main__':
	main()