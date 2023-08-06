#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/2/1 9:32
@File    : export_strategy_setting.py
@contact : mmmaaaggg@163.com
@desc    : 用于导出 策略设置 生成 json 文件，该文件用于覆盖
.vntrader\cta_strategy_setting.json
.vntrader\portfolio_strategy_setting.json
文件
"""
import json
import os
import uuid
from collections import OrderedDict
from datetime import date
from typing import List, Union

from ibats_utils.mess import date_2_str

from vnpy_extra.constants import INSTRUMENT_TYPE_SUBSCRIPTION_DIC
from vnpy_extra.db.orm import AccountStrategyMapping
from vnpy_extra.utils.enhancement import get_instrument_type


def generate_setting_dic(vt_symbols: Union[str, list], strategy_class_name: str,
                         strategy_settings: dict, short_name=None) -> (str, dict, bool):
    """生成 cta/portfolio setting dict数据"""
    if isinstance(vt_symbols, str):
        vt_symbols = vt_symbols.split('_')

    if not short_name:
        short_name = f"{strategy_class_name}_" \
                     f"{'_'.join([_.split('.')[0] for _ in vt_symbols])}_{uuid.uuid4().hex}"

    if len(vt_symbols) == 1:
        is_cta = True
        setting_dic = OrderedDict()
        setting_dic["class_name"] = strategy_class_name
        setting_dic["vt_symbol"] = get_vt_symbols_4_subscription(vt_symbols[0])
        setting_dic["setting"] = settings = OrderedDict()
        settings['class_name'] = strategy_class_name
        for k, v in strategy_settings.items():
            settings[k] = v
    else:
        is_cta = False
        setting_dic = OrderedDict()
        setting_dic["class_name"] = strategy_class_name
        setting_dic["vt_symbols"] = [get_vt_symbols_4_subscription(_) for _ in vt_symbols]
        setting_dic["setting"] = settings = OrderedDict()
        for k, v in strategy_settings.items():
            settings[k] = v

    settings.setdefault('base_position', 1)
    settings.setdefault('stop_opening_pos', 0)
    return short_name, setting_dic, is_cta


def get_vt_symbols_4_subscription(vt_symbols):
    """获取可进行行情订阅的合约代码"""
    instrument_type = get_instrument_type(vt_symbols)
    subscription_type = INSTRUMENT_TYPE_SUBSCRIPTION_DIC[instrument_type.upper()]
    return subscription_type + vt_symbols[len(instrument_type):]


def generate_strategy_setting_file():
    """生成策略配置文件"""
    stg_list: List[AccountStrategyMapping] = AccountStrategyMapping.get_by_account()
    cta_dic = OrderedDict()
    portfolio_dic = OrderedDict()
    for stats in stg_list:
        # symbols = stats.symbols_info.symbols
        # vt_symbols = symbols.split('_')
        # if len(vt_symbols) == 1:
        #     cta_dic[stats.short_name] = dic = OrderedDict()
        #     dic["class_name"] = stats.stg_info.strategy_class_name
        #     dic["vt_symbol"] = get_vt_symbols_4_subscription(vt_symbols[0])
        #     dic["setting"] = settings = OrderedDict()
        #     settings['class_name'] = stats.stg_info.strategy_class_name
        #     for k, v in stats.strategy_settings.items():
        #         settings[k] = v
        # else:
        #     portfolio_dic[stats.short_name] = dic = OrderedDict()
        #     dic["class_name"] = stats.stg_info.strategy_class_name
        #     dic["vt_symbols"] = [get_vt_symbols_4_subscription(_) for _ in vt_symbols]
        #     dic["setting"] = settings = OrderedDict()
        #     for k, v in stats.strategy_settings.items():
        #         settings[k] = v
        #
        # if 'base_position' not in settings:
        #     settings['base_position'] = 1
        # if 'stop_opening_pos' not in settings:
        #     settings['stop_opening_pos'] = 0
        symbols = stats.symbols_info.symbols
        strategy_class_name = stats.stg_info.strategy_class_name
        strategy_settings = stats.strategy_settings
        short_name = stats.short_name
        short_name, settings, is_cta = generate_setting_dic(symbols, strategy_class_name, strategy_settings, short_name)
        if is_cta:
            cta_dic[short_name] = settings
        else:
            portfolio_dic[short_name] = settings

    folder_path = os.path.join("output", "strategy_settings", date_2_str(date.today()))
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "cta_strategy_setting.json")
    with open(file_path, 'w') as f:
        json.dump(cta_dic, f, indent=4)

    file_path = os.path.join(folder_path, "portfolio_strategy_setting.json")
    with open(file_path, 'w') as f:
        json.dump(portfolio_dic, f, indent=4)


if __name__ == "__main__":
    pass
