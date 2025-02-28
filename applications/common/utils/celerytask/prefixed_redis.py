# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/25
Description: <Brief description of the file>
"""
import redis

class GlobalKeyPrefixMixin:
    def __init__(self, *args, global_prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_prefix = global_prefix or ''

    def _add_prefix(self, key):
        return f"{self.global_prefix}:{key}" if self.global_prefix else key

    def get(self, name, *args, **kwargs):
        return super().get(self._add_prefix(name), *args, **kwargs)

    def set(self, name, value, *args, **kwargs):
        return super().set(self._add_prefix(name), value, *args, **kwargs)

    def delete(self, *names, **kwargs):
        return super().delete(*[self._add_prefix(name) for name in names], **kwargs)

    # 添加其他需要的方法...

class PrefixedStrictRedis(GlobalKeyPrefixMixin, redis.Redis):
    pass