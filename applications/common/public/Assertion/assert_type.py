"""
-*- coding: utf-8 -*-

@Author : carlos
@Time : 2023/captchacode/24 16:04
@file_tool : assert_type.py
@talk : 干什么的？
"""

import logging
import time

from assertpy import assert_that
from public.logging_tool.log_control import INFO, ERROR ,WARNING


# 初始化日志配置


def check_assertstr(check_value=None, expect_value=None, assert_type=None,timeout=1.5,count=None):
    """
    使用assertpy库进行断言
    失败重试可以添加 for 循环去执行。
    :param check_value: 待判断的值
    :param expect_value: 期望的值
    :param assert_type: 断言类型，可选值包括:
                        - 'is_length': 判断长度是否等于期待值
                        - 'is_not_empty': 判断值不为空
                        - 'is_equal_to': 判断值是否等于期待值
                        - 'is_not_equal_to': 判断值是否不等于期待值
                        - 'contains': 判断值是否包含期待值
                        - 'contains_ignoring_case': 不区分大小写判断值是否包含期待值
                        - 'does_not_contain': 判断值是否不包含期待值
                        - 'starts_with': 判断值是否以期待值开头
                        - 'ends_with': 判断值是否以期待值结尾
                        - 'fuzzy_query ' : 模糊查询的判断方法 即 结果值集合的每个是包含期望值的
    """
    # 打印测试值、期待值和断言类型
    INFO.logger.info(f'测试值为 {check_value}，断言方式：{assert_type}，期待值为：{expect_value}')


    try:
        # 根据不同的断言类型使用assertpy进行断言
        if assert_type == 'is_length':
            assert_that(check_value).is_length(expect_value)  # 判断长度是否等于期待值

        elif assert_type == 'is_not_empty':
            assert_that(check_value).is_not_empty()  # 判断值不为空

        elif assert_type == 'is_equal_to':
            assert_that(check_value).is_equal_to(expect_value)  # 判断值是否等于期待值

        elif assert_type == 'is_not_equal_to':
            assert_that(check_value).is_not_equal_to(expect_value)  # 判断值是否不等于期待值

        elif assert_type == 'contains':
            if isinstance(expect_value,list):
                for itme in expect_value:
                    assert_that(check_value).contains(itme)
            assert_that(check_value).contains(*expect_value)  # 判断值是否包含期待值

        elif assert_type == 'contains_ignoring_case':
            assert_that(check_value).contains_ignoring_case(*expect_value)  # 不区分大小写判断值是否包含期待值

        elif assert_type == 'does_not_contain':
            if isinstance(expect_value,list):
                for itme in expect_value:
                    assert_that(check_value).does_not_contain(itme)
            assert_that(check_value).does_not_contain(expect_value)  # 判断值是否不包含期待值

        elif assert_type == 'starts_with':
            assert_that(check_value).starts_with(expect_value)  # 判断值是否以期待值开头


        elif assert_type == 'ends_with':
            assert_that(check_value).ends_with(expect_value)  # 判断值是否以期待值结尾


        elif assert_type == 'fuzzy_query': # 模糊查询 结果（集合）值 包含期望值
            if isinstance(expect_value,list):
                for itme in expect_value:
                    assert_that(check_value).contains(itme)
            else:
                assert_that(expect_value).contains(*check_value)  # 判断 期待值是否包含 结果值

        else :
            ERROR.logger.error(f'不支持的断言类型：{assert_type}')
            assert False

        return True
    except :

        if count is None:
            ERROR.logger.error(f'判断失败,请检查代码，或者添加失败重试操作。')
            assert False
        elif count==2:
            ERROR.logger.error(f'重新执行{count+1}次失败了,请检查代码')
            assert False

        WARNING.logger.warning(f'判断错误，重新执行，强制等待时间间隔为{timeout}秒')
        time.sleep(timeout)

        # else:
        #     ERROR.logger.error(f'请检查代码!!!,并添加新的可能信息')
        #     assert False



    # INFO.logger.info('断言 测试通过！！！')

if __name__ == '__main__':

    # check_assertstr('foo', 3, 'is_length')  # 验证字符串长度是3
    # check_assertstr('foo', None, 'is_not_empty')  # 验证非空
    #
    # check_assertstr('foo', 'foo', 'is_equal_to')  # 验证相同
    # check_assertstr('foo', 'bar', 'is_not_equal_to')  # 验证不相同

    check_assertstr('foo', ['f', 'oo'], 'contains')  # 验证包含字符和字符串
    # check_assertstr(['99','66','foo'], ['foo', '66','5'], 'contains')  # 验证包含字符和字符串
    # check_assertstr('foo', ['F', 'oO'], 'contains_ignoring_case')  # 验证忽略大小写包含字符和字符串
    # check_assertstr(['foo','bb'], 'bb1', 'does_not_contain')  # 验证不包含该字符
    # check_assertstr(['foo', 'bb'], ['foo', 'bb'], 'does_not_contain')  # 验证不包含该字符
    # # check_assertstr('foo', 'f', 'starts_with')  # 验证以f字符开始
    # # check_assertstr('foo', 'oo', 'ends_with')  # 验证以oo字符串结束

    a=check_assertstr('foo', ['f', 'oo'], 'contains')

    print(a)
