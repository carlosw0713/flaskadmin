# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/13
Description: <Brief description of the file>
"""
import datetime
from applications.extensions import db
from sqlalchemy import Column, JSON, String, DateTime

# 数据库模型定义
class JobInfo(db.Model):
    __tablename__ = 'job_info'
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(50), nullable=False,comment="任务名称")
    cron_expression = db.Column(db.String(50), nullable=False,comment="cron表达式")
    script_id = db.Column(db.Integer, db.ForeignKey('script_info.id'), nullable=False,comment="脚本id")
    script_name = db.Column(db.String(50), nullable=False,comment="脚本名称")
    notification_config = db.Column(JSON,comment="通知配置")
    job_status = db.Column(db.String(50), nullable=False,comment="任务状态")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')



class JobLog(db.Model):
    __tablename__ = 'job_log'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_info.id'), nullable=False,comment="脚本id")
    log_content = db.Column(db.Text, nullable=False,comment="日志信息")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')