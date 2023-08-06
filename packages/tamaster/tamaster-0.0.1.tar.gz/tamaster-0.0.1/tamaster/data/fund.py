from dataclasses import dataclass
from datetime import date

@dataclass
class FundNav:
    """产品净值"""
    fund_name: str = None                      # 基金名称
    fund_code: str = None                      # 基金代码
    net_value: float = None                    # 单位净值
    accumulated_net_value: float = None        # 累计净值
    net_value_date: date = None                # 净值日期
    asset_amount: float = None                 # 资产净值
    asset_volume: float = None                 # 资产份额
