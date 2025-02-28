# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/24
Description: <Brief description of the file>
"""
import datetime
import json

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Blueprint, jsonify,request

from applications.models.ems.job import JobInfo
from applications.models.ems.script import ScriptInfo
from apscheduler.triggers.interval import IntervalTrigger


from concurrent.futures import ThreadPoolExecutor


bp = Blueprint('scheduler', __name__, url_prefix='/scheduler')

# 初始化操作，启动调度任务
scheduler=BackgroundScheduler()
scheduler.start()


def run_method(script_path,auth_info,input_params):
    '''
    执行方法
    :param envpath:
    :param fun_name:
    :param Kwargs:
    :return:
    '''

    # 获取函数对象
    fun_name = str(script_path).split('.')[-1]
    envpath = str(script_path).split(f'.{fun_name}')[0]
    fun_obj = get_method_object(envpath, fun_name)



    try:

        result = fun_obj(dict_escape(auth_info),dict_escape(input_params))  # 直接调用
        return result
    except Exception as e:
        return (f"方法执行异常: {e}")


def get_method_object(envpath, fun_name):
    """
    获取指定环境下的可调方法对象

    :param envpath: 完整的环境配置模块路径（如 settings.hlzy.apiauth.dev.local）
    :param fun_name: 要获取的方法名
    :return: 可调用的方法对象
    :raises ImportError: 模块加载失败
    :raises AttributeError: 方法或模块未找到
    :raises TypeError: 找到的不是可调方法
    """
    try:
        # 动态导入模块
        module = __import__(envpath, fromlist=[fun_name])
    except ImportError as e:
        raise ImportError(f"模块加载失败: {envpath}") from e

    try:
        # 获取方法对象
        method = getattr(module, fun_name)
    except AttributeError as e:
        raise AttributeError(f"方法未找到: {envpath}.{fun_name}") from e

    if not callable(method):
        raise TypeError(f"非可调方法: {envpath}.{fun_name}")

    return method

def dict_escape(s):
    '''
    字符串转json
    :param s:
    :return:
    '''
    try:
        # 替换单引号为双引号
        s_fixed = s.replace("'", '"')
        # 转换为字典
        data = json.loads(s_fixed)
        return data
    except Exception as e:
        return {}


@bp.post('/add/<int:job_id>')
def add_scheduler(job_id):
    '''
    新增计划
    :return:
    '''

    # job_data = JobInfo.query.get(id=job_id) # 必须通过主键查询
    job_data = JobInfo.query.filter_by(id=job_id).first() #	可通过任意字段过滤
    script_data = ScriptInfo.query.filter_by(id = job_data.script_id).first()

    # 判断脚本状态
    job_status = job_data.job_status
    if not job_status:
        return jsonify({'message': '任务状态不为True，不执行调度任务的添加'}), 400

    # 解析时间表达式
    cron_expression = job_data.cron_expression
    try:
        second, minute, hour, day, month, day_of_week = cron_expression.split()
    except ValueError:
        return jsonify({'message': 'Invalid cron expression format'}), 400


    # 获取函数对象
    fun_name = str(script_data.script_path).split('.')[-1]
    envpath = str(script_data.script_path).split(f'.{fun_name}')[0]
    fun_obj = get_method_object(envpath, fun_name)

    # kwargsinfo 调度信息的入参信息
    kwargsinfo={'notification_config': dict_escape(job_data.notification_config),
     'auth_info': dict_escape(script_data.auth_info), 'input_params': dict_escape(script_data.input_params)}

    # 添加到调度器
    scheduler.add_job(
        func=fun_obj,
        trigger='cron',
        id=str(job_data.id),
        # args=argsinfo,
        kwargs=kwargsinfo,
        max_instances=1,
        replace_existing=True,

        # 定时执行参数
        second=second,
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week,
    )

    return jsonify({'message': '添加调度任务成功',
                    'job_id':f'{job_id}'}), 200


@bp.post('/init')
def init_scheduler():

    jobidlist=[]

    for job_data in JobInfo.query.all():

        add_scheduler(job_data.id)


        jobidlist.append(str(job_data.id))


    return jsonify({'message': '调度器初始化成功',
                    'job_idlist':f'{jobidlist}'}), 200

@bp.post('delete/<int:job_id>')
def delete_scheduler(job_id):
    try:
        scheduler.remove_job(str(job_id))
        return {"message": f"调度任务{job_id}删除成功"}, 200
    except Exception as e:
        return {"message": f"删除任务异常{e}"}, 400

@bp.post('update/<int:job_id>')
def update_scheduler(job_id):
    delete_scheduler(job_id)
    add_scheduler(job_id)

    return {"message": f"调度任务{job_id}更新成功"}, 200

@bp.post('/start')
def start_scheduler():
    """启动调度器"""
    try:
        scheduler.start()  # 通过app属性访问调度器
        return jsonify({'message': '调度器已启动'}), 200
    except Exception as e:
        return jsonify({'error': f'启动失败: {str(e)}'}), 500

@bp.post('/stop')
def stop_scheduler():
    """停止调度器"""
    try:

        scheduler.shutdown()
        return jsonify({'message': '调度器已停止'}), 200
    except Exception as e:
        return jsonify({'error': f'停止失败: {str(e)}'}), 500

if __name__ == '__main__':
    pass