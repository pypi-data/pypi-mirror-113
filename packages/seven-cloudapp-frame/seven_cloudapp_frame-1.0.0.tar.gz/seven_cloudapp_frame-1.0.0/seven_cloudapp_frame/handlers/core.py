# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2021-07-15 14:09:43
@LastEditTime: 2021-07-19 13:58:42
@LastEditors: HuangJianYi
:description: 通用Handler
"""
from seven_cloudapp_frame.handlers.frame_base import *


class IndexHandler(FrameBaseHandler):
    """
    :description: 默认页
    """
    def get_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: HuangJingCan
        """
        self.write(UUIDHelper.get_uuid() + "_" + config.get_value("run_port") + "_api")