#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# __name__ = str2_md5.py
import hashlib

def getStrAsMD5(parmStr):
    # parmStr参数必须是utf8
    if isinstance(parmStr,str):
        # 如果是unicode先转utf-8
        parmStr=parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest().upper()
