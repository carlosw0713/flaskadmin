# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/13
Description: <Brief description of the file>
"""

from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from applications.models import ScriptInfo


class ScriptInfoOutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ScriptInfo  # table = models.Album.__table__
        # include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
        include_fk = True  # 序列化阶段是否也一并返回主键
        # fields= ["id","name"] # 启动的字段列表
        # fields= ["name","id"] # 启动的字段列表
        # exclude = ["id","name"] # 排除字段列表
