"""
-*- coding: utf-8 -*-

@Author : carlos
@Time : 2023/11/17 14:25
@File : ding_talk.py
@talk : 钉钉通知封装
"""


import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any, Text
from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink


class DingTalkSendMsg:

    """ 发送钉钉通知 """
    timeStamp = str(round(time.time() * 1000))
    img_url='https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png'
    webhook="https://oapi.dingtalk.com/robot/send?access_token=d93246056e51aed5a10bc70daad371de93557d4f1b41d5662c0506dc0e306932"
    secret= "SECe47d5a33a263cfc88e9a667c46da0cf7854fd683cd84cebe31e7e524b8b60cc4"

    def xiao_ding(self):
        sign = self.get_sign()
        # 从yaml文件中获取钉钉配置信息
        webhook = self.webhook + "&timestamp=" + self.timeStamp + "&sign=" + sign
        return DingtalkChatbot(webhook)

    def get_sign(self) -> Text:
        """
        根据时间戳 + "sign" 生成密钥
        :return:
        """
        string_to_sign = f'{self.timeStamp}\n{self.secret}'.encode('utf-8')
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign,
            digestmod=hashlib.sha256).digest()

        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_text(
            self,
            msg: Text,
            mobiles=None
    ) -> None:
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: 艾特用户电话
        :return:
        """
        if not mobiles:
            self.xiao_ding().send_text(msg=msg, is_at_all=True)
        else:
            if isinstance(mobiles, list):
                self.xiao_ding().send_text(msg=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def send_link(
            self,
            title: Text,
            text: Text,
            message_url: Text,
            pic_url: Text
    ) -> None:
        """
        发送link通知
        :return:
        """
        self.xiao_ding().send_link(
                title=title,
                text=text,
                message_url=message_url,
                pic_url=pic_url
            )

    def send_markdown(
            self,
            title: Text,
            msg: Text,
            mobiles=None,
            is_at_all=False
    ) -> None:
        """

        :param is_at_all:
        :param mobiles:
        :param title:
        :param msg:
        markdown 格式
        """

        if mobiles is None:
            self.xiao_ding().send_markdown(title=title, text=msg, is_at_all=is_at_all)
        else:
            if isinstance(mobiles, list):
                self.xiao_ding().send_markdown(title=title, text=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    @staticmethod
    def feed_link(
            title: Text,
            message_url: Text,
            pic_url: Text
    ) -> Any:
        """ FeedLink 二次封装 """
        return FeedLink(
            title=title,
            message_url=message_url,
            pic_url=pic_url
        )

    def send_feed_link(self, *arg) -> None:
        """发送 feed_lik """
        self.xiao_ding().send_feed_card(list(arg))

    def send_ding_notification(self,noticetext):
        """ 发送钉钉报告通知
        注意需要开启钉钉，并且测试报告含失败的
        """
        # 判断如果有失败的用例，@所有人

        text = noticetext
        DingTalkSendMsg().send_markdown(
            title="【标题目录】",
            msg=f"{text}\n"
                f" ![screenshot](" \
                f"{self.img_url}" \
                f")",
            is_at_all=True # 判断如果有失败的用例，@所有人
        )


if __name__ == '__main__':

    task=DingTalkSendMsg()
    task.send_ding_notification(noticetext='测试发送消息')