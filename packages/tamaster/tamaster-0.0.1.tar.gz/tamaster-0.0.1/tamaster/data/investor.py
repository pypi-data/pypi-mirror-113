from dataclasses import dataclass
from datetime import date

@dataclass
class InvestorInfo:
    """投资者信息"""
    investor_name: str = None                  # 投资者名称
    investor_type: str = None                  # 投资者类型
    certificate_type: str = None               # 投资者证件类型
    certificate_number: str = None             # 投资者证件号码
    fund_account_number: str = None            # 基金账号
    trade_account_number: str = None           # 交易账号
    trade_account_open_date: date = None       # 交易账号开户日期
    bank_account_name: str = None              # 银行账户名称
    bank_account_number: str = None            # 银行账号
    bank_name: str = None                      # 开户行名称
    phone: str = None                          # 联系电话
    email: str = None                          # 电子邮箱
    address: str = None                        # 通讯地址
    postcode: str = None                       # 邮编
    agency_name: str = None                    # 销售商名称
    agency_code: str = None                    # 销售商代码

@dataclass
class InvestorShare:
    """投资者持有份额"""
    investor_name: str = None                  # 投资者名称
    investor_type: str = None                  # 投资者类型
    certificate_type: str = None               # 投资者证件类型
    certificate_number: str = None             # 投资者证件号码
    fund_account_number: str = None            # 基金账号
    trade_account_number: str = None           # 交易账号
    fund_name: str = None                      # 基金名称
    fund_code: str = None                      # 基金代码
    total_share: float = None                  # 总份额
    available_share: float = None              # 可用份额
    frozen_share: float = None                 # 冻结份额
    share_date: date = None                    # 份额持有日期
    agency_name: str = None                    # 销售商名称
    agency_code: str = None                    # 销售商代码
    structured_fund_name: str = None           # 分级基金名称
    structured_fund_code: str = None           # 分级基金代码
    dividend_method: str = None                # 分红方式
