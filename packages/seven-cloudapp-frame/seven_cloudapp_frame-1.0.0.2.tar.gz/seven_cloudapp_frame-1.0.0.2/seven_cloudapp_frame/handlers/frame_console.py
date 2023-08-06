# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-19 13:37:16
@LastEditTime: 2021-07-23 10:59:17
@LastEditors: HuangJianYi
@Description: 
"""
import threading, multiprocessing
from seven_framework.console.base_console import *
from seven_cloudapp_frame.libs.customize.seven_helper import *

from seven_cloudapp_frame.models.db_models.asset.asset_warn_config_model import *
from seven_cloudapp_frame.models.db_models.asset.asset_warn_notice_model import *
from seven_cloudapp_frame.models.db_models.user.user_asset_model import *
from seven_cloudapp_frame.models.db_models.asset.asset_inventory_model import *


class FrameConsole():
    """
    :description: 控制台基类
    """
    def console_asset_warn(self, mod_count=10, sub_table_count=0):
        """
        :description: 控制台资产预警
        :param mod_count: 单表队列数
        :param sub_table_count: 分表数
        :return: 
        :last_editors: HuangJianYi
        """
        if sub_table_count == 0:

            self._start_process_user_asset_warn(None,mod_count)
            self._start_process_asset_inventory_warn(None, mod_count)

        else:

            for i in range(sub_table_count):

                t = multiprocessing.Process(target=self._start_process_user_asset_warn, args=[str(i), mod_count])
                t.start()

                j = multiprocessing.Process(target=self._start_process_asset_inventory_warn, args=[str(i), mod_count])
                j.start()

    def _start_process_user_asset_warn(self, sub_table, mod_count):

        for i in range(mod_count):

            t = threading.Thread(target=self._process_user_asset_warn, args=[sub_table, i, mod_count])
            t.start()

    def _start_process_asset_inventory_warn(self, sub_table, mod_count):

        for i in range(mod_count):

            j = threading.Thread(target=self._process_asset_inventory_warn, args=[sub_table, i, mod_count])
            j.start()

    def _process_user_asset_warn(self,sub_table,mod_value, mod_count):
        """
        :description: 处理用户资产负数预警
        :param sub_table: 分表名称
        :param mod_value: 当前队列值
        :param mod_count: 队列数
        :return: 
        :last_editors: HuangJianYi
        """
        user_asset_model = UserAssetModel(sub_table=sub_table)
        asset_warn_notice_model = AssetWarnNoticeModel()
        now_date = TimeHelper.get_now_format_time()
        now_day_int = SevenHelper.get_now_day_int()
        print(f"{TimeHelper.get_now_format_time()} 用户资产负数预警队列{mod_value}启动")
        while True:
            user_asset_list = user_asset_model.get_list(f"MOD(act_id,{mod_count})={mod_value} and asset_value<0 and {now_day_int}>warn_day ", order_by="create_date asc", limit="100")
            if len(user_asset_list) > 0:
                for user_asset in user_asset_list:
                    try:
                        user_asset.warn_date = now_date
                        user_asset.warn_day = now_day_int
                        user_asset_model.update_entity(user_asset, "warn_date,warn_day")

                        asset_warn_notice = AssetWarnNotice()
                        asset_warn_notice.app_id = user_asset.app_id
                        asset_warn_notice.act_id = user_asset.act_id
                        asset_warn_notice.user_id = user_asset.user_id
                        asset_warn_notice.open_id = user_asset.open_id
                        asset_warn_notice.user_nick = user_asset.user_nick
                        asset_warn_notice.asset_type = user_asset.asset_type
                        asset_warn_notice.asset_object_id = user_asset.asset_object_id
                        if user_asset.asset_type == 1:
                            asset_warn_notice.log_title = f"次数异常,值为负数:{user_asset.asset_value}"
                        elif user_asset.asset_type == 2:
                            asset_warn_notice.log_title = f"积分异常,值为负数:{user_asset.asset_value}"
                        else:
                            asset_warn_notice.log_title = f"档位异常,档位ID:{user_asset.asset_object_id},值为负数:{user_asset.asset_value}"

                        asset_warn_notice.info_json = SevenHelper.json_dumps(user_asset)
                        asset_warn_notice.create_date = now_date
                        asset_warn_notice.create_day = now_day_int
                        asset_warn_notice_model.add(asset_warn_notice)

                    except Exception as ex:
                        logger_error.error(f"用户资产负数预警队列{mod_value}异常,json串:{user_asset_list.decode()},ex:{ex.decode()}")
                        continue
            else:
                time.sleep(60)

    def _process_asset_inventory_warn(self,sub_table, mod_value, mod_count):
        """
        :description: 处理资产每日进销存是否对等预警
        :param sub_table: 分表名称
        :param mod_value: 当前队列值
        :param mod_count: 队列数
        :return: 
        :last_editors: HuangJianYi
        """
        asset_inventory_model = AssetInventoryModel()
        asset_warn_notice_model = AssetWarnNoticeModel()
        now_date = TimeHelper.get_now_format_time()
        now_day_int = SevenHelper.get_now_day_int()
        print(f"{TimeHelper.get_now_format_time()} 资产每日进销存预警队列{mod_value}启动")
        while True:
            asset_inventory_list = asset_inventory_model.get_list(f"MOD(act_id,{mod_count})={mod_value} and create_day={now_day_int} and process_count=0", order_by="create_date asc", limit="100")
            if len(asset_inventory_list) > 0:
                for asset_inventory in asset_inventory_list:
                    try:
                        asset_inventory.process_count = 1
                        asset_inventory.process_date = now_date
                        asset_inventory_model.update_entity(asset_inventory, "process_count,process_date")

                        if (asset_inventory.history_value + asset_inventory.inc_value + asset_inventory.dec_value) != asset_inventory.now_value:

                            asset_warn_notice = AssetWarnNotice()
                            asset_warn_notice.app_id = asset_inventory.app_id
                            asset_warn_notice.act_id = asset_inventory.act_id
                            asset_warn_notice.user_id = asset_inventory.user_id
                            asset_warn_notice.open_id = asset_inventory.open_id
                            asset_warn_notice.user_nick = asset_inventory.user_nick
                            asset_warn_notice.asset_type = asset_inventory.asset_type
                            asset_warn_notice.asset_object_id = asset_inventory.asset_object_id
                            asset_warn_notice.log_title = f"历史值:{asset_inventory.history_value},增加：{asset_inventory.inc_value},减少：{asset_inventory.dec_value},当前值:{asset_inventory.now_value}"
                            if asset_inventory.asset_type == 1:
                                asset_warn_notice.log_title = "次数每日进销存异常," + asset_warn_notice.log_title
                            elif asset_inventory.asset_type == 2:
                                asset_warn_notice.log_title = "积分每日进销存异常," + asset_warn_notice.log_title
                            else:
                                asset_warn_notice.log_title = f"价格档位每日进销存异常,档位ID:{asset_inventory.asset_object_id},"+ asset_warn_notice.log_title

                            asset_warn_notice.info_json = SevenHelper.json_dumps(asset_inventory)
                            asset_warn_notice.create_date = now_date
                            asset_warn_notice.create_day = now_day_int
                            asset_warn_notice_model.add(asset_warn_notice)

                    except Exception as ex:
                        logger_error.error(f"资产每日进销存预警队列{mod_value}异常,json串:{asset_inventory_list.decode()},ex:{ex.decode()}")
                        continue
            else:
                time.sleep(60*60)
