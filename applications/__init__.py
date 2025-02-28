import os

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask
from applications.common.script import init_script
from applications.config import BaseConfig
from applications.extensions import init_plugs
from applications.view import init_bps


from applications.common.HLZY import init_hlzyscript


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    # 引入配置
    app.config.from_object(BaseConfig)

    # 注册flask组件
    init_plugs(app)

    # 注册蓝图
    init_bps(app)

    # 注册命令
    init_script(app)

    # # 注测脚本
    init_hlzyscript(app)


    return app


