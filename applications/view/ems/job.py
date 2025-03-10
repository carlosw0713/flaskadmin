# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/13
Description: <Brief description of the file>
"""
from flask import Blueprint, render_template, request, jsonify,current_app


from applications.common.utils.http import success_api, fail_api,table_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db

from applications.models import JobInfo,JobLog
from applications.schemas import JobInfoOutSchema

from concurrent.futures import ThreadPoolExecutor

# 获取调度任务中的方法
from applications.view.ems.Scheduler import add_scheduler,delete_scheduler,update_scheduler

bp = Blueprint('job', __name__, url_prefix='/job')


@bp.get('/log/')
@authorize("ems:joblog:main")
def joblog_index():
    return render_template('system/photo/photo.html')

@bp.get('/log/page')
@authorize("ems:joblog:page")
def joblog_page():
    '''
    job日志列表
    '''

    job_id = str_escape(request.args.get('job_id', type=str))

    dbinfopage=JobLog.query.filter_by(job_id=job_id)

    data = [dbinfo.to_dict(only=['job_id', 'create_at']) for dbinfo in dbinfopage.items]

    return table_api(data=data, count=dbinfopage.total)

@bp.get('/log/add')
# @authorize("ems:joblog:add")
def joblog_save():
    '''
    job日志列表
    '''

    req = request.get_json(force=True)

    # 简化写法
    data = {
        'job_id': str_escape(req.get('job_id')),
        'log_content': str_escape(req.get('log_content')),
    }

    jobloginfo=JobLog(**data)

    db.session.add(jobloginfo)
    db.session.commit(jobloginfo)

    return success_api(msg="添加日志成功")

@bp.get('/log/remove/<int:job_id>')
def joblog_remove(job_id):
    '''
    根据任务id删除任务日志
    '''
    jobloginfo = JobLog.query.filter_by(job_id=job_id).delete()

    db.session.commit()

    if not jobloginfo:
        return fail_api(msg="删除job日志失败")
    return success_api(msg="删除job日志成功")


# ———————————————————————————————————————————————————————————————————————————

@bp.get('/')
@authorize("ems:job:main")
# def jobinfo_index():
def main():
    return render_template('ems/job/main.html')

@bp.get('/page')
# @authorize("ems:jobinfo:page")
def jobinfo_page():

    job_name = str_escape(request.args.get('job_name', type=str))
    job_status = str_escape(request.args.get('job_status', type=str))
    script_name = str_escape(request.args.get('script_name', type=str))

    filters = []

    if job_name:
        filters.append(JobInfo.job_name.contains(job_name))
    if job_status:
        filters.append(JobInfo.job_status.contains(job_status))
    if script_name:
        filters.append(JobInfo.script_name.contains(script_name))
    # print("查询内容",filters)
    roles = JobInfo.query.filter(*filters).layui_paginate()

    # ORM的序列化功能
    data=JobInfoOutSchema(many=True).dump(roles)

    return table_api(data=data, count=roles.total)

@bp.get('/add')
# @authorize("ems:jobinfo:add", log=True)
def add():
    return render_template('ems/job/add.html')

@bp.post('/save')
# @authorize("system:jobinfo:add", log=True)
def save():
    req = request.get_json(force=True)

    # 简化写法
    job_data = {
        'job_name': str_escape(req.get('job_name')),
        'cron_expression': str_escape(req.get('cron_expression')),
        'notification_config': req.get('notification_config'),
        'script_name': str_escape(req.get('script_name')),
        'script_id': str_escape(req.get('script_id')),
        'job_status': str_escape(req.get('job_status'))
    }

    jobinfo = JobInfo(**job_data)

    db.session.add(jobinfo)
    db.session.commit()

    executor = ThreadPoolExecutor(max_workers=2)
    executor.submit(add_scheduler, jobinfo.id)
    # 新增调度任务

    return success_api(msg="成功")


@bp.get('/edit/<int:id>')
# @authorize("system:jobinfo:add", log=True)
def edit(id):
    dbinfo = JobInfo.query.filter_by(id=id).first()

    # 简化写法
    data=JobInfoOutSchema(many=False).dump(dbinfo)

    return render_template('ems/job/edit.html',data=data)


@bp.post('/update')
# @authorize("system:jobinfo:edit", log=True)
def update():
    req = request.get_json(force=True)

    id = req.get('id')

    # 简化写法
    job_data = {
        'job_name': str_escape(req.get('job_name')),
        'cron_expression': str_escape(req.get('cron_expression')),
        'notification_config': req.get('notification_config'),
        'script_name': str_escape(req.get('script_name')),
        'script_id': str_escape(req.get('script_id')),
        'job_status': str_escape(req.get('job_status'))
    }

    jobinfo = JobInfo(**job_data)

    result=JobInfo.query.filter_by(id=id).update(job_data)
    db.session.commit()

    # 更新调度任务
    # executor = ThreadPoolExecutor(max_workers=2)
    # executor.submit(update_scheduler, jobinfo.id)

    update_scheduler(id)

    if not result:
        return fail_api(msg="更新任务失败")
    return success_api(msg="更新任务成功")


@bp.delete('/remove/<int:id>')
@authorize("system:jobinfo:remove", log=True)
def remove(id):
    # role = JobInfo.query.filter_by(id=id).first()

    # 删除这个任务下所有的日志
    # XXXXXXXXXXXXXXX

    r = JobInfo.query.filter_by(id=id).delete()
    db.session.commit()

    # 删除调度任务
    executor = ThreadPoolExecutor(max_workers=2)
    executor.submit(delete_scheduler,  id)

    if not r:
        return fail_api(msg="任务删除失败")
    return success_api(msg="任务删除成功")


@bp.get('/cron')
def cron_expression():

    return render_template('ems/job/cron.html')

