#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/8 09:21
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @file_tool    : curlchange这是真的.py
# @IDE     : PyCharm
# @REMARKS : 备注
import re

import requests
requestSession = requests.Session()
# 设置所有的请求都将不验证SSL证书
requestSession.verify = False

class ApiWay():
    def CurlGenerateCode(self,curl):

        cookies = {
            'Hm_lvt_75a21f203d323a988b1d8ce0eeae4de5': '1731304563',
            'Hm_lpvt_75a21f203d323a988b1d8ce0eeae4de5': '1731304563',
            'HMACCOUNT': 'F434B1C40CA6C00D',
            '__gads': 'ID=8abf4325f3202ec4:T=1731304561:RT=1731304561:S=ALNI_MaUzspzTr8473v8aQRENdgRP5hKYA',
            '__gpi': 'UID=00000f90f13c9cdb:T=1731304561:RT=1731304561:S=ALNI_MapzbO_0dsZrPuB4O93U8PACOB0MA',
            '__eoi': 'ID=e3a71418d008dc93:T=1731304561:RT=1731304561:S=AA-AfjZHtTRGmJ7JQKHiQ_GR45o6',
        }

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'Hm_lvt_75a21f203d323a988b1d8ce0eeae4de5=1731304563; Hm_lpvt_75a21f203d323a988b1d8ce0eeae4de5=1731304563; HMACCOUNT=F434B1C40CA6C00D; __gads=ID=8abf4325f3202ec4:T=1731304561:RT=1731304561:S=ALNI_MaUzspzTr8473v8aQRENdgRP5hKYA; __gpi=UID=00000f90f13c9cdb:T=1731304561:RT=1731304561:S=ALNI_MapzbO_0dsZrPuB4O93U8PACOB0MA; __eoi=ID=e3a71418d008dc93:T=1731304561:RT=1731304561:S=AA-AfjZHtTRGmJ7JQKHiQ_GR45o6',
            'origin': 'https://www.lddgo.net',
            'priority': 'u=1, i',
            'referer': 'https://www.lddgo.net/convert/curl-to-code',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        json_data = {
            'code': curl,
            'lang': 'python',
        }

        response = requestSession.post('https://www.lddgo.net/api/CurlGenerateCode', cookies=cookies, headers=headers,
                                 json=json_data)

        resp=response.json()
        # print(resp)

        if resp['code']==0:
            print('curl转换成功')
            pass
        else:
            print(f'curl转换失败',resp)
            assert 1>2


        resp=str(resp).replace('\\n', '')
        resp=str(resp).replace('\\', '')


        # try:
        #     response_text=re.findall(r'(response = .*? json=json_data)', str(resp))[0]+")"
        #     json_text = re.findall(r'(json_data = {.*?})', str(resp))[0]
        # except:
        #     response_text=re.findall(r'(response = .*? headers=headers)', str(resp))[0]+")"
        #     json_text = re.findall(r'(params = {.*?})', str(resp))[0]

        try:
            response_text = re.findall(r'(response = .*? json=json_data)', str(resp))[0] + ")"
            json_text = re.findall(r'(json_data = {.*?})', str(resp))[0]
        except:
            try:
                json_text = re.findall(r'(params = {.*?})', str(resp))[0]
                response_text = re.findall(r'(response = .*? headers=headers)', str(resp))[0] + ")"
            except IndexError:
                print("未找到匹配的响应或参数")
                json_text = ""
                response_text = re.findall(r'(response = .*? headers=headers)', str(resp))[0] + ")"
            except Exception as inner_e:
                print(f"二次尝试匹配失败: {inner_e}")
                json_text = ""
                response_text = re.findall(r'(response = .*? headers=headers)', str(resp))[0] + ")"


        # print(json_text)

        return resp,json_text,response_text

    def curlchanggetopythonmodel(self,curl):
        '''
        将curl 转换为python代码，并提取出user-token、url、brand-id等参数
        :return:
        '''

        resp,json_text,response_text=self.CurlGenerateCode(curl)
        try :
            uri=re.findall(r"(https:.*?com)", curl)[0]
        except:
            #可能不是.COM
            uri=re.findall(r"(https:.*?cn)", response_text)[0]

        url=str(re.findall(r"('https:.*?')",response_text)[0]).replace("'","")
        urlpathstring=str(url.split(f'{uri}')[1]).replace('/','')
        urlpathstring=urlpathstring.replace('api','') #路径中可能有api

        response_model=str(response_text)
        response_model=response_model.replace('requests','requestSession')
        response_model=response_model.replace('=cookies','=self.cookies')
        response_model=response_model.replace('=headers','=self.headers')

        response_model=response_model.replace("'http","f'http")
        response_model=response_model.replace(f'{uri}','{self.uri}')

        response_all=(f"def {urlpathstring}(self):\n\n"
                      f"\t{json_text}\n"
                      f"\t{response_model}\n")

        assert_data='''
    resp=response.json()
    curl=generate_curl_command(response)
    if resp.get('code')==0:
        INFO.logger.info(f"成功，返回信息：{resp}")
        return resp
    else:
        ERROR.logger.error(f"失败，返回信息：{resp}")'''

        response_all+=assert_data
        print(response_all)


        with open('curl转化后文件.txt', 'w') as f:
            f.write(response_all)
            print('curl转化信息文件写入成功')

    def getcurlinfo(self):


        curl_request = '''
        curl 'https://sss-test.sh-internal.com/api/default/share/exclusion/rule/manage/detail' \
          -H 'Accept: application/json' \
          -H 'Accept-Language: zh-CN,zh;q=0.9' \
          -H 'Connection: keep-alive' \
          -H 'Content-Type: application/json;charset=UTF-8' \
          -H 'Cookie: _ga=GA1.1.55056312.1719484292; user-token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJ1c2VySWRcIjoxN30iLCJpYXQiOjE3MTk0ODQ0MzYsImV4cCI6MzgwMDc0ODQ0MzZ9.r6pwPmb4NTziWlZUJxuapC15_k37eQmjYxYIt1HLKbYs89FxitWfuIBCMV8DLhMXjrxHDLbTpLuH5DgADngTIQ; _ga_RDDML5PE08=GS1.1.1720063712.7.1.1720063844.0.0.0; acw_tc=1a0c380a17204015956431936e0044cd99e9791da174d80343d1abcf81266b; _ga_MCV17FG4H6=GS1.1.1720401595.22.1.1720401597.0.0.0' \
          -H 'Origin: https://sss-test.sh-internal.com' \
          -H 'Referer: https://sss-test.sh-internal.com/' \
          -H 'Sec-Fetch-Dest: empty' \
          -H 'Sec-Fetch-Mode: cors' \
          -H 'Sec-Fetch-Site: same-origin' \
          -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' \
          -H 'brand-id: 6533' \
          -H 'sec-ch-ua: "Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"' \
          -H 'sec-ch-ua-mobile: ?0' \
          -H 'sec-ch-ua-platform: "macOS"' \
          -H 'user-token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJ1c2VySWRcIjoxN30iLCJpYXQiOjE3MTk0ODQ0MzYsImV4cCI6MzgwMDc0ODQ0MzZ9.r6pwPmb4NTziWlZUJxuapC15_k37eQmjYxYIt1HLKbYs89FxitWfuIBCMV8DLhMXjrxHDLbTpLuH5DgADngTIQ' \
          --data-raw '{"brandId":6533,"memberId":17,"userName":"string","userPhone":"17855337260","operator":"string"}'
        '''

        # 使用正则表达式提取 user-token 和 URL
        url_pattern = re.compile(r"curl\s+'([^']*)'")
        user_token_pattern = re.compile(r"user-token=([^;]*)")

        url_match = url_pattern.search(curl_request)
        user_token_match = user_token_pattern.search(curl_request)

        if url_match:
            url = url_match.group(1)
            print(f"URL: {url}")

        if user_token_match:
            user_token = user_token_match.group(1)
            print(f"user-token: {user_token}")

    def changecurltoapi(self,curl_command):
        '''
        更改curl的值
        url、curl、user-token、band_id
        :param curl_command:
        :return:
        '''

        # 提取 user-token 和 brand-id 的正则表达式
        user_token_regex = r'user-token=([^;]+)'
        brand_id_regex = r'brand-id: (\d+)'
        url_regex = r"curl\s+'([^']*)'"

        # 使用正则表达式提取 user-token 和 brand-id 的值
        user_token_match = re.search(user_token_regex, curl_command)
        brand_id_match = re.search(brand_id_regex, curl_command)
        url_match = re.search(url_regex, curl_command)

        if user_token_match and brand_id_match:
            user_token = user_token_match.group(1)
            brand_id = brand_id_match.group(1)
            url = url_match.group(1)
            uri = re.findall(r'(http.*?.com)', url)[0]

            # # 替换 curl 命令中的占位符为变量的值
            updated_curl_command = curl_command.replace(brand_id, '${{brand-id}}')
            updated_curl_command = updated_curl_command.replace(user_token, '${{user-token}}')
            # updated_curl_command = updated_curl_command.replace(url, '{{url}}')
            updated_curl_command = updated_curl_command.replace(uri, '${{uri}}')
            print(updated_curl_command)
            # print(user_token)
            return updated_curl_command


        else:
            print("无法提取 user-token 或 brand-id")
            exit(1)


    def runcurlcreatetask(self):
        '''
        执行创建curl文件
        1.读取文件中curl
        2.通过通用接口转化提取respone、jsondata
        3.自定义模版妆化
        4.生成配置文件
        :return:
        '''

        with open('curl转化文件', 'r', encoding='utf-8') as f:
            curl_command=f.read()
            task.curlchanggetopythonmodel(curl=curl_command)

            # 生成转化的的curl文件
            self.changecurltoapi(curl_command)




if __name__ == '__main__':

    task=ApiWay()

    task.runcurlcreatetask()









