# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/20
Description: <Brief description of the file>
"""
import json
import re
import shlex

def print_dict_line_by_line(input_dict):
    """
    将字典中的键值对按每行显示。

    参数:
    input_dict (dict): 要打印的字典。

    返回:
    None
    """
    input_dict=json.loads(input_dict)
    dictstring="{"
    for key, value in input_dict.items():

        if isinstance(value, str):
            value = f"'{value}'"

        dictstring+=f"\n\t\t'{key}': {value},"

    dictstring+="\n\t\t}"

    return dictstring

def curlconverter_way(curl_command):
    '''
    将curl信息转化
    :param curl_command:
    :return:
    '''


    parsed = shlex.split(curl_command)
    method = parsed[0]
    url = parsed[1]
    headers = {}
    data = None

    for i in range(2, len(parsed)):
        if parsed[i] == "-H":
            herader = parsed[i + 1].replace("'", "")
            headers[herader.split(": ")[0]] = herader.split(": ")[1]

        elif parsed[i] == "--compressed" or parsed[i] == "--data-raw":
            data = parsed[i + 1]
        else:
            pass

    return {'method': method, 'url': url, 'headers': headers, 'data': data}


def apimodel(curl_command):
    '''
    根据curl信息获取curl转化后的api模板数据
    :param curl_command:
    :return:
    '''

    curlinfo = curlconverter_way(curl_command)
    hearders = curlinfo.get('headers')
    data = curlinfo.get('data')
    url=curlinfo.get('url')
    try:
        uri=re.findall('(http.*?.com)',url)[0]
    except:
        uri=re.findall('(http.*?.cn)',url)[0]

    method=curlinfo.get('method')
    if method=='curl':
        method='post'
    elif method=='get':

        data=url.split('?')
        url=data[0]
        if len(data)>1:
            from_data=data[1]
            for i in from_data.split('&'):
                try:
                    data[i.split('=')[0]]=i.split('=')[1]
                except Exception as e:
                    print(e)
        else:
            data=None
    else:
        Exception('不支持该请求方式')

    return {'uri':uri,'url':url,'method':method,'data':data,'headers':hearders}

def request_scripy(curl_command):
    '''
    获取 request模板
    :param curl_command:
    :return:
    '''

    requestinfo=apimodel(curl_command)

    uri=requestinfo.get('uri')
    url=requestinfo.get('url')
    method=requestinfo.get('method')
    headers=requestinfo.get('headers')
    data=requestinfo.get('data')

    urlpath=url.split(uri)[1]
    urlpathstring=urlpath.replace('/','')
    urlpathstring=urlpathstring.replace('api','')

    method_defname=f"def {urlpathstring}(self):\n\n"

    if data is not None:
        if method=='get':
            params=data
            params = print_dict_line_by_line(input_dict=params)
            json_text=f"\tjson_data={params}\n\n"
            response_text=f"\tresponse=requestSession.{method}(f'{url}',headers={headers},params=json_data)"
            response_text=response_text.replace(f"{url}","{self.uri}"+urlpath)
            response_text=response_text.replace(f"{headers}","{self.headers}"+urlpath)


        else:
            data = print_dict_line_by_line(input_dict=data)
            json_text=f"\tjson_data={data}\n\n"
            response_text = f"\tresponse=requestSession.{method}(f'{url}',headers={headers},data=json_data)"
            response_text = response_text.replace(f"{url}", "{self.uri}" + urlpath)
            response_text = response_text.replace(f"{headers}", "{self.headers}")

    else:
        json_text = f""
        response_text = f"\tresponse=requestSession.{method}(f'{url}',headers={headers},data=json_data)"
        response_text = response_text.replace(f"{url}", "{self.uri}" + urlpath)
        response_text = response_text.replace(f"{headers}", "{self.headers}")



    assert_data='''\n
    resp=response.json()
    curl=generate_curl_command(response)
    if resp.get('code')==0:
        INFO.logger.info(f"成功，返回信息：{resp}")
        return resp
    else:
        ERROR.logger.error(f"失败，返回信息：{resp}")'''

    response_all=method_defname+json_text+response_text+assert_data

    print(response_all)

if __name__ == '__main__':
    curl_command="""curl 'https://676baa14979de6bc68a4db8d.iot.heilansc.com:83/v1/api/dsconfig' \
  -X 'PUT' \
  -H 'Accept: application/json' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'Authorization: Bearer l60of7Lf48V4Hm0nG5GZN0uSkdkM8Pch' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: jxl_ga=GA1.1.1342519037.1733798712; jxl_ga_3YK6Y5HC9N=GS1.1.1733798711.1.1.1733799482.0.0.0; hb_MA-B8B4-DCBCC6752B4F_source=op.heilansc.cn' \
  -H 'Origin: https://676baa14979de6bc68a4db8d.iot.heilansc.com:83' \
  -H 'Referer: https://676baa14979de6bc68a4db8d.iot.heilansc.com:83/edge-computing/apps/device/cloud' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0' \
  -H 'sec-ch-ua: "Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"device_supervisor":{"clouds":{"0000676cf497bbff":{"_id":"0000676cf497bbff","name":"苏南码头正式环境","type":"Standard MQTT","cacheSize":10000,"enable":1,"args":{"host":"222.191.251.12","port":1883,"clientId":"HLGW1012426003172","auth":1,"tls":0,"cleanSession":0,"mqttVersion":"v3.1.1","keepalive":60,"key":"","cert":"","rootCA":"","verifyServer":0,"verifyClient":0,"username":"HLGW1012426003172@hlsc","passwd":"HLGW1012426003172&hlsc","willQos":0,"willRetain":0,"willTopic":"","willPayload":""}}}}}'"""






    request_scripy(curl_command)





