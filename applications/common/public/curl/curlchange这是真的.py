# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/6
Description: <Brief description of the file>
"""


# -*-coding:gbk-*-
import argparse
import json
from shlex import split
from urllib.parse import urlparse

from w3lib.http import basic_auth_header


class CurlParser(argparse.ArgumentParser):
    def error(self, message):
        error_msg = \
            'There was an error parsing the curl command: {}'.format(message)
        raise ValueError(error_msg)


curl_parser = CurlParser()
curl_parser.add_argument('url')
curl_parser.add_argument('-H', '--header', dest='headers', action='append')
curl_parser.add_argument('-X', '--request', dest='method', default='post')
curl_parser.add_argument('-d', '--data-raw', dest='data')
curl_parser.add_argument('-u', '--user', dest='auth')

safe_to_ignore_arguments = [
    ['--compressed'],
    ['-s', '--silent'],
    ['-v', '--verbose'],
    ['-#', '--progress-bar']
]
for argument in safe_to_ignore_arguments:
    curl_parser.add_argument(*argument, action='store_true')


def curl_to_request_kwargs(curl_command, ignore_unknown_options=True):
    """Convert a cURL command syntax to Request kwargs.
    :param str curl_command: string containing the curl command
    :param bool ignore_unknown_options: If true, only a warning is emitted when
    cURL options are unknown. Otherwise raises an error. (default: True)
    :return: dictionary of Request kwargs
    """
    curl_args = split(curl_command)
    if curl_args[0] != 'curl':
        raise ValueError('A curl command must start with "curl"')
    parsed_args, argv = curl_parser.parse_known_args(curl_args[1:])
    if argv:
        msg = 'Unrecognized options: {}'.format(', '.join(argv))
    url = parsed_args.url

    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url
    result = {'method': parsed_args.method.upper(), 'url': url}
    headers = []
    cookies = {}
    for header in parsed_args.headers or ():
        name, val = header.split(':', 1)
        name = name.strip()
        val = val.strip()
        headers.append((name, val))
    if parsed_args.auth:
        user, password = parsed_args.auth.split(':', 1)
        headers.append(('Authorization', basic_auth_header(user, password)))
    if headers:
        result['headers'] = dict(headers)
    if cookies:
        result['cookies'] = cookies
    if parsed_args.data:
        result['body'] = json.loads(parsed_args.data)
        result['body_type'] = 2
    return result

if __name__ == '__main__':
    # 忽略未知参数
    curl_command = """
                    curl --location -g --request GET '{{baseUrl}}/api/v1/ps/get?l=22&kj=5' \
                    --header 'ab: 11' \
                    --header 'fg: dfg' \
                    --header "Content-Type: text/plain" \
                    --data-raw '{"s": 0}'
                   """
    result = curl_to_request_kwargs(curl_command)

    # 不忽略未知参数
    result2 = curl_to_request_kwargs(curl_command, False)

    print(result
          ,'\n',result2)
