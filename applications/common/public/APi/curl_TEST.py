import requests

import re

# 创建一个全局的Session对象
requestSession = requests.Session()
# 设置所有的请求都将不验证SSL证书
requestSession.verify = False
def parse_curl_command(curl_command):
    """
    从curl命令字符串中解析请求头、请求体和URL信息

    参数:
    curl_command (str): 包含curl命令的字符串

    返回:
    dict: 包含URL、请求头和请求体信息的字典
    """
    # 初始化结果字典
    result = {
        'url': '',
        'headers': {},
        'data': ''
    }

    # 提取URL
    url_pattern = r'\'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\''
    url_match = re.search(url_pattern, curl_command)
    if url_match:
        result['url'] = url_match.group(1)

    # 提取请求头
    header_pattern = r'--header\s+\'(.*?)\''
    headers_matches = re.findall(header_pattern, curl_command)
    for header in headers_matches:
        key, value = header.split(': ', 1)
        result['headers'][key] = value

    # 提取请求体
    data_pattern = r'--data-binary\s+\'(.*?)\''
    data_match = re.search(data_pattern, curl_command)
    if data_match:
        result['data'] = data_match.group(1)

    return result


def CurlGenerateCode(code,lang='python'):

    cookies = {
        'Hm_lvt_75a21f203d323a988b1d8ce0eeae4de5': '1719570240,1720002643,1720662554',
        'Hm_lpvt_75a21f203d323a988b1d8ce0eeae4de5': '1720662554',
        'HMACCOUNT': '6710851ADE38ABB8',
        '__gads': 'ID=933121bf0c8632cc:T=1719570240:RT=1720662554:S=ALNI_Ma9SXiLrCmViulkCyOjG6ZbUNv5_w',
        '__gpi': 'UID=00000e69ad94593e:T=1719570240:RT=1720662554:S=ALNI_MaX2bxI2rYuKilcBha7K9yF6b_k-g',
        '__eoi': 'ID=a54ef9179131bd7a:T=1719570240:RT=1720662554:S=AA-Afja0MDSwiFb8SQAwChmOd3ge',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'Hm_lvt_75a21f203d323a988b1d8ce0eeae4de5=1719570240,1720002643,1720662554; Hm_lpvt_75a21f203d323a988b1d8ce0eeae4de5=1720662554; HMACCOUNT=6710851ADE38ABB8; __gads=ID=933121bf0c8632cc:T=1719570240:RT=1720662554:S=ALNI_Ma9SXiLrCmViulkCyOjG6ZbUNv5_w; __gpi=UID=00000e69ad94593e:T=1719570240:RT=1720662554:S=ALNI_MaX2bxI2rYuKilcBha7K9yF6b_k-g; __eoi=ID=a54ef9179131bd7a:T=1719570240:RT=1720662554:S=AA-Afja0MDSwiFb8SQAwChmOd3ge',
        'origin': 'https://www.lddgo.net',
        'priority': 'u=1, i',
        'referer': 'https://www.lddgo.net/convert/curl-to-code',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'code': code,
        'lang': lang,
    }

    response = requestSession.post('https://www.lddgo.net/api/CurlGenerateCode', cookies=cookies, headers=headers, json=json_data)
    resp=response.json()
    print(resp.get('data')
    )

if __name__ == '__main__':
    curlcode="""curl 'https://iiot-tk-4u.heilansc.cn/api/iot/product' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Authorization: Bearer d55a8615-3417-495a-8950-2707b629123a' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: access_token=d55a8615-3417-495a-8950-2707b629123a' \
  -H 'Origin: https://iiot-tk-4u.heilansc.cn' \
  -H 'Referer: https://iiot-tk-4u.heilansc.cn/products/productCenter' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36' \
  -H 'X-Biz-App-Name: IOT' \
  -H 'sec-ch-ua: "Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"deviceType":1,"productCode":"6tigy2q0","productName":"carlos_网关主设备100","protocolCode":"HLSC_MQTT","remark":"111111111111111"}'"""
    print(CurlGenerateCode(code=curlcode))
    parsed_info = parse_curl_command(curlcode)
