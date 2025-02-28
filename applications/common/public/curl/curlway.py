# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/29
Description: <Brief description of the file>
"""

import re
import subprocess


def run_curl(curl_command):
    """
    运行给定的 curl 命令并返回输出结果。

    :param curl_command: str, 完整的 curl 命令字符串
    :return: tuple, (stdout_output, stderr_output)
    """
    try:
        # 使用 shell=True 来允许通过字符串直接执行命令
        result = subprocess.run(curl_command, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)

        # 获取标准输出和标准错误输出
        stdout_output = result.stdout
        stderr_output = result.stderr

        return stdout_output, stderr_output
    except subprocess.CalledProcessError as e:
        # 如果 curl 命令返回非零退出状态，这里会捕获异常
        print(f"An error occurred while running the curl command: {e}")
        return None, e.stderr


def parse_curl(curl_command):
    """
    解析 curl 命令，提取 URL、请求方式、请求头、请求体和 URI 等信息。

    :param curl_command: str, 完整的 curl 命令字符串
    :return: dict, 包含解析结果的字典
    """
    result = {
        'url': None,
        'method': 'GET',  # 默认为 GET 请求
        'headers': {},
        'data': None,
        'uri': None
    }

    # 提取 URL
    url_match = re.search(r'curl\s+([\'"]?)(http[s]?://[^\'"\s]+)\1', curl_command)
    if url_match:
        result['url'] = url_match.group(2)
        result['uri'] = url_match.group(2).split('?')[0]

    # 提取请求方式
    method_match = re.search(r'-X\s+(\w+)', curl_command)
    if method_match:
        result['method'] = method_match.group(1)

    # 提取请求头
    header_pattern = r'-H\s+([\'"]?)([^\'"\s]+):\s*([^\'"\s]+)\1'
    headers = re.findall(header_pattern, curl_command)
    for header in headers:
        key = header[1].strip()
        value = header[2].strip()
        result['headers'][key] = value

    # 提取请求体
    data_match = re.search(r'--data(-raw)?\s+([\'"]?)([^\'"]+)\2', curl_command)
    if data_match:
        result['data'] = data_match.group(3)

    return result
if __name__ == '__main__':

    # 示例用法
    curl_command = """curl 'https://cn.bing.com/AS/Suggestions?pt=page.serp&bq=%E7%99%BE%E5%BA%A6&mkt=zh-cn&ds=mobileweb&qry=%E7%99%BE%E5%BA%A6&cp=2&csr=1&zis=1&msbqf=false&rqry=1&pths=1&cvid=00ABC3596D36400286C5F27008F25344' \
  -H 'accept: */*' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'cookie: MUID=3D43237FB7DD66730D043701B6C467C0; SRCHD=AF=SHORUN; SRCHUID=V=2&GUID=C32E0125EB234B17BEEAD081E76CDE9C&dmnchg=1; MUIDB=3D43237FB7DD66730D043701B6C467C0; MSPTC=DakYE7VBqAJNsuoipXKJzP99HHO8a3ZVPUmTULroJBE; NAP=V=1.9&E=1e3d&C=gshkmack6XZ5OFV1FcZcG8I-Glm8BCQ6foW0BeuSPykRkUiFHymSyQ&W=1; _Rwho=u=d&ts=2025-02-07; _SS=SID=0F695361C59D6203385E46EDC4FB6369&PC=CNNDDB&R=200&RB=200&GB=0&RG=0&RP=200; _EDGE_S=SID=0F695361C59D6203385E46EDC4FB6369&ui=zh-cn; _clck=hpomp6%7C2%7Cft9%7C0%7C1865; USRLOC=HS=1&ELOC=LAT=31.310758590698242|LON=121.51190185546875|N=%E6%9D%A8%E6%B5%A6%E5%8C%BA%EF%BC%8C%E4%B8%8A%E6%B5%B7%E5%B8%82|ELT=6|&BID=MjUwMjEyMDQ0MjQ2Xzc5M2Q0YTc3YjJiNjJkYWE4ODcyNzFiYjVmM2NiOGZkNDExY2Y2OWQ0ZjU1MWI2YTE0MWRkMjgwZmYzNjU4NjI=; _uetsid=23573b20e82411ef8cd0f7eb0f7f9f6d; _uetvid=eff21b50b5e711ef9748b7433823af9b; _uetmsclkid=_uet43e891a3ea5c1411ff66f605a5d24740; SRCHUSR=DOB=20241106&T=1739324792000; .MSA.Auth=CfDJ8M3eg4IpuVdJrTR-axYKM_Q6ArJG-ex5SDg_PCVsW-8MHxMLRK0SozkruuNmp0hN_rcwynIy46gph26RtJ61L0Aw2XqX7d9jwCd-j6YSquvAlm_rUEhJlHFtve0WyW4i_1sUvGAitKn1YeyQ17Ky6BW8i9tnW8Sn4Ogqr8jLGc1HOC7G8TxCj39I4r470Z1zuhlE09V8bG5EPtYd2dhUbDrKAdioKB1398iQ7KxuA1MOlixCz1rmLNNPzvdXg9Z-SaP_hqp1la5HsSBGCv6gpzUJHALw0484XqV8v01hpHbAqF5WURWMsxs73ASYn2uWDnz1UdqltFJ1tImshwVAU1fbPSEVcABPlL6IFWNIFAqv148uqTStNFHrKh7ve_GIeXsj93Q74NnRDMS0TXSNSVY; SNRHOP=I=&TS=; _U=17tJ74ir2_cetFY4PNohC8yjhDglUlWcNOESwz4Ize1w0E7BnktzdyiFBdnND44BTP-vSixU8vuTK5PPzkBIa0dLQGKR5TeSasGLA10RyRbLSSzThu5ht_Wse89vusXorF5liLo2HgpaxBS5TKCtoqC-w50Cn5w_LE3Gtlywmg7uC91TIz1tOdsDmiMR9kcMyjQNhDsjNysBvjYvwZGN2MqkxVVQx6G7gn_u01i_5f3w; ANON=A=0000C45C920AA8895501C7A5FFFFFFFF; WLS=C=aaa0b25edabecc32&N=%e6%b5%a9%e9%93%ad; GC=JwT5t3d1Y_obFIWLMGaDkPZCRK7BMlbIelZWXooAKv29vF9WeVZx3fh8e5tIbEjxrTUwsn_H9xNdUwDnUFKauQ; SRCHHPGUSR=SRCHLANG=zh-Hans&PV=10.0.0&BZA=0&DM=0&BRW=W&BRH=M&CW=1452&CH=1000&SCW=1437&SCH=3659&DPR=1.3&UTC=480&EXLTT=32&HV=1739328087&PRVCW=2000&PRVCH=1000&AV=14&ADV=14&RB=0&MB=0&NTWKTYP=4g; _RwBf=mta=0&rc=200&rb=200&gb=0&rg=0&pc=200&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=4&l=2025-02-11T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=-62135539200&rwflt=-62135539200&rwaul2=0&o=0&p=MSAAUTOENROLL&c=MR000T&t=8016&s=2023-09-28T06:29:25.3573879+00:00&ts=2025-02-12T02:41:25.8524479+00:00&rwred=0&wls=0&wlb=0&wle=1&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&e=JA19gJKFHQXJyRJeDR1x3_d2qR-EGp4AIp98MrMmfRFl4ofE7BHUdV351u5966ZFP3K-tmJsC--v5-bdACbCwLMUqPJ2atx6kYKJj77zNDI&A=0000C45C920AA8895501C7A5FFFFFFFF' \
  -H 'ect: 4g' \
  -H 'priority: u=1, i' \
  -H 'referer: https://cn.bing.com/search?filters=ufn%3a%22%e7%99%be%e5%ba%a6%22+sid%3a%228cbad010-9cf5-000a-f0dd-0815861f3c88%22&qs=MB&pq=baidu&sk=CSYN1UAS5SC11&sc=20-5&pglt=161&q=%E7%99%BE%E5%BA%A6&cvid=88af352966844b23b6b9869fc67237f3&gs_lcrp=EgRlZGdlKgYIARAuGEAyBggAEEUYOTIGCAEQLhhAMgYIAhAuGEAyBggDEEUYPDIGCAQQRRg8MgYIBRBFGDwyBggGEEUYQTIGCAcQRRhBMgYICBBFGEHSAQgyNDQxajBqMagCALACAA&FORM=ANNTA1&PC=CNNDDB' \
  -H 'sec-ch-ua: "Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"' \
  -H 'sec-ch-ua-arch: "x86"' \
  -H 'sec-ch-ua-bitness: "64"' \
  -H 'sec-ch-ua-full-version: "132.0.2957.140"' \
  -H 'sec-ch-ua-full-version-list: "Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.160", "Microsoft Edge";v="132.0.2957.140"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-model: ""' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-ch-ua-platform-version: "10.0.0"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-ms-gec: 6AC5B8598C3977669C4C5B9B994D38BF3EDCEAB60E6DA4BF38222647A811223A' \
  -H 'sec-ms-gec-version: 1-132.0.2957.140' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0' \
  -H 'x-autosuggest-contentwidth: 650' \
  -H 'x-client-data: eyIxIjoiMCIsIjIiOiIwIiwiMyI6IjAiLCI0IjoiLTU0MTQ5MDEzNTUyMzcyNjc2MjAiLCI2Ijoic3RhYmxlIiwiOSI6ImRlc2t0b3AifQ==' \
  -H 'x-edge-shopping-flag: 1'"""


    parsed_result = parse_curl(curl_command)
    print(parsed_result)


    # print(run_curl(curl_command=curl_command))
