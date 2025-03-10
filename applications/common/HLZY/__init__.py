# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/17
Description: <Brief description of the file>
"""

import warnings
# 禁用InsecureRequestWarning警告
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings('ignore', category=InsecureRequestWarning)
import requests
# 创建一个全局的Session对象
requestSession = requests.Session()
# 设置所有的请求都将不验证SSL证书
requestSession.verify = False
from applications.common.public.logging_tool.log_control import *

def loginmodel(logininfo):
    '''
    登录模板
    :param data:
    :return:
    '''

    host=logininfo['host']

    data=logininfo['data']


    if "iot" in host:
        AppName="IOT"
    elif "ems" in host:
        AppName="EMS"
    else:
        print(f"地址输入有误，缺少ems和iot相关信息")

    if "phone" in data.keys():
        grant_type="phone"
    elif "username" in data.keys():
        grant_type="password"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Authorization': 'Basic bmVidXZlaWw6bmVidXZlaWw=',
        'Connection': 'keep-alive',
        'Origin': f'{host}',
        'Referer': f'{host}/login',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'X-Biz-App-Name': f'{AppName}',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'skipToken': 'true',
    }

    params = {
        'randomStr': 'blockPuzzle',
        'code': 'sHsHbRlkFkktV1gwsLoOqAHidsy0d/2vuoc7L4r9Zrw3Qaj3QNCo1DKXeN46LGl2OVbXjOZx/hlO3OkNpAkQN4hbExeFqjLk0MPULrk24YM=',
        'grant_type': f'{grant_type}', #注意grant_type
        'scope': 'server',
    }

    response = requests.post(f'{host}/api/auth/oauth2/token', params=params, headers=headers,
                             data=data)

    method = response.request.method
    url = response.request.url
    uri = response.request.headers.get('Origin', None)

    resp = response.json()
    tenant_id = resp.get('tenant_id')
    access_token = f"{resp.get('access_token')}"

    headers['Authorization'] = f"Bearer {resp.get('access_token')}"
    headers['TENANT-ID'] = tenant_id

    print(f"登录成功，uri:{uri},\n 手机号:{data.get('phone')},tenant_id:{tenant_id},access_token:{access_token}")
    print(response.json())
    authinfo = {
        'uri': uri,
        'headers': headers,
        'cookies': {
            'access_token': access_token,
            'tenant_id': tenant_id,
        }
    }

    return authinfo

# 构建蓝图
from flask import Flask, Blueprint
from applications.common.HLZY.IOT.way.device.iotdevicealarm import bp as iotdevicealarm_bp

hlzyscript_bp = Blueprint('hlzyscript', __name__, url_prefix='/hlzyscript')
def init_hlzyscript(app: Flask):
    hlzyscript_bp.register_blueprint(iotdevicealarm_bp)

    app.register_blueprint(hlzyscript_bp)


