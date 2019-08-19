import requests
from proxypool.setting import TEST_URL

proxy = '180.149.96.131:8080'
print(proxy)

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

print(TEST_URL)
response = requests.get(TEST_URL, proxies=proxies, verify=False)
if response.status_code == 200:
    print('Successfully')
    print(response.text.encode('utf-8'))
else:
    print('bad request')
