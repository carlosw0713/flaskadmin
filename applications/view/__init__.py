from applications.view.system import register_system_bps
from applications.view.plugin import register_plugin_views

from applications.view.ems import register_ems_bps

def init_bps(app):

    register_system_bps(app)
    register_plugin_views(app)

    # ems初始蓝图
    register_ems_bps(app)
