#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/15 13:04
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : verificationcodeway.py
# @IDE     : PyCharm
# @REMARKS : 备注
import ddddocr
from captcha.image import ImageCaptcha
from io import BytesIO
from PIL import Image
from random import choices


def gen_captcha(content='0123456789',k=4):
    """ 生成验证码 """
    image = ImageCaptcha()
    # 获取字符串
    captcha_text = "".join(choices(content, k=k))
    # 生成图像
    captcha_image = Image.open(image.generate(captcha_text))
    return captcha_text, captcha_image


if __name__ == '__main__':


    # 对ddddocr进行实例化

    ocr = ddddocr.DdddOcr()

    sum=100
    sum1=100
    sussess=0
    for i in range(100):
        # 读取文件
        k=4
        text,image = gen_captcha(k=k)

        res = ocr.classification(image)
        if len(res)!=k:
            sum1-=1

        if text == res:
            sussess+=1

        print( f"期望结果：{text}，实际结果{res}")

    print(f"识别成功率：{sussess/sum:.2%}")
    print(f"优惠后成功率：{sussess/sum1:.2%}")




