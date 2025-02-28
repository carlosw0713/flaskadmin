# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/13
Description: <Brief description of the file>
"""


from flask import Blueprint, render_template, request, jsonify

from applications.common import curd
from applications.common.utils import validate
from applications.common.utils.http import success_api, fail_api,table_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db


from applications.models import ScriptInfo
from applications.schemas import ScriptInfoOutSchema

# 获取调度任务中的方法
from applications.view.ems.Scheduler import run_method

bp = Blueprint('script', __name__, url_prefix='/script')

@bp.get('/')
@authorize("ems:scriptinfo:main")
def main():
    return render_template('ems/script/main.html')


@bp.get('/page')
@authorize("ems:script:page")
def script_page():
    '''
    脚本信息列表
    '''

    script_name = str_escape(request.args.get('script_name', type=str))

    filters = []

    if script_name:
        filters.append(ScriptInfo.script_name.contains(script_name))


    dbinfo= ScriptInfo.query.filter(*filters).layui_paginate()

    # print(dbinfo)
    data = ScriptInfoOutSchema(many=True).dump(dbinfo)

    return table_api(data=data, count=dbinfo.total)


@bp.get('/add')
@authorize("ems:scriptinfo:add", log=True)
def add():
    return render_template('ems/script/add.html')


@bp.post('/save')
@authorize("ems:scriptinfo:save", log=True)
def save():

    req = request.get_json(force=True)

    # 简化写法
    json_data = {
        'task_type': str_escape(req.get('task_type')),
        'script_name': str_escape(req.get('script_name')),
        'script_desc': str_escape(req.get('script_desc')),
        'auth_info': req.get('auth_info'),
        'input_params': req.get('input_params'),
        'script_path': str_escape(req.get('script_path'))
    }

    dbinfo = ScriptInfo(**json_data)

    db.session.add(dbinfo)
    db.session.commit()

    return success_api(msg= "成功")



@bp.get('/edit/<int:id>')
# @authorize("system:user:edit", log=True)
def edit(id):


    # ScriptInfo.query.filter_by(id=1).first():
    # 这个查询返回的是一个单一的对象（如果找到匹配的记录）或者
    # None（如果没有找到匹配的记录）。
    # 返回的结果是一个具体的
    # ScriptInfo
    # 实例。
    # ScriptInfo.query.filter_by(id=1):
    # 这个查询返回的是一个
    # Query
    # 对象，而不是直接返回查询结果。
    # 你需要进一步调用.all()
    # 或者其他方法来获取实际的数据列表。


    dbinfo = ScriptInfo.query.filter_by(id=id).first()


    # 移除 many=True 参数：如果你只需要序列化单个对象，则不需要使用 many=True。
    data = ScriptInfoOutSchema(many=False).dump(dbinfo)
    return render_template('ems/script/edit.html',scriptinfo=data)


@bp.post('/update')
# @authorize("ems:scriptinfo:edit", log=True)
def update():
    req = request.get_json(force=True)

    id = req.get('id')

    # 简化写法
    json_data = {
        'task_type': str_escape(req.get('task_type')),
        'script_name': str_escape(req.get('script_name')),
        'script_desc': str_escape(req.get('script_desc')),
        'auth_info': req.get('auth_info'),
        'input_params': req.get('input_params'),
        'script_path': str_escape(req.get('script_path'))
    }

    # dbinfo = ScriptInfo(**json_data)

    result = ScriptInfo.query.filter_by(id=id).update(json_data)

    db.session.commit()

    if not result:
        return fail_api(msg="更新脚本失败")
    return success_api(msg="更新脚本成功")

@bp.post('/remove/<int:id>')
# @authorize("ems:scriptinfo:remove", log=True)
def remove(id):
    # role = ScriptInfo.query.filter_by(id=id).first()

    # 删除这个任务下所有的日志
    # XXXXXXXXXXXXXXX

    r = ScriptInfo.query.filter_by(id=id).delete()
    db.session.commit()
    if not r:
        return fail_api(msg="脚本删除失败")
    return success_api(msg="脚本删除成功")


@bp.get('/debug/<int:id>')
def debuginfo(id):

    dbinfo = ScriptInfo.query.filter_by(id=id).first()

    # 移除 many=True 参数：如果你只需要序列化单个对象，则不需要使用 many=True。
    data = ScriptInfoOutSchema(many=False).dump(dbinfo)
    return render_template('ems/script/debug.html',scriptinfo=data)

@bp.post('/debug/run')
def rundebug():
    '''
    调试脚本
    :return:
    '''

    req = request.get_json(force=True)


    result= run_method(
        script_path=req.get('script_path'),
            auth_info = req.get('auth_info'),
            input_params= req.get('input_params')

                            )

    return jsonify({'message': '方法调试成功', 'result': result}), 200
