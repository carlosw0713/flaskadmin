# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/13
Description: <Brief description of the file>
"""
import datetime
from sqlalchemy import Column, JSON, String, DateTime

from applications.extensions import db

class ScriptInfo(db.Model):
    __tablename__ = 'script_info'
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String(50), nullable=False)
    script_name = db.Column(db.String(50), nullable=False,comment="脚本名称")
    script_desc = db.Column(db.String(500), nullable=False,comment="脚本描述")
    # auth_info = db.Column(db.String(500),comment="用户验证")
    auth_info = db.Column(JSON,comment="用户验证")
    input_params = db.Column(JSON,comment="输入项")
    script_path = db.Column(db.String(200), nullable=False,comment="路径")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
    # cron_jobs = db.relationship('job_info', backref='script_info', lazy=True)
