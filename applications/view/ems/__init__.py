# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/13
Description: <Brief description of the file>
"""

from flask import Flask, Blueprint

from applications.view.ems.job import bp as jobbp
from applications.view.ems.script import bp as scriptbp
from applications.view.ems.Scheduler import bp as scheduler

ems_bp = Blueprint('ems', __name__, url_prefix='/ems')


def register_ems_bps(app: Flask):
    ems_bp.register_blueprint(jobbp)
    ems_bp.register_blueprint(scriptbp)
    ems_bp.register_blueprint(scheduler)


    # 添加蓝图
    # app.register_blueprint(index_bp)
    app.register_blueprint(ems_bp)


