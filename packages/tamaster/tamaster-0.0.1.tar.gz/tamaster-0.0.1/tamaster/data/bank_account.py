from dataclasses import dataclass
from datetime import datetime

@dataclass
class BankAccount:
    """银行账户余额"""
    fund_name: str = None                      # 基金名称
    fund_code: str = None                      # 基金代码
    bank_account_name: str = None              # 银行账户名称
    bank_account_number: str = None            # 银行账号
    bank_name: str = None                      # 开户行名称
    balance: float = None                      # 账户余额
    available: float = None                    # 可用余额
    currency: str = None                       # 币种
    description: str = None                    # 说明
    update_time: datetime = None               # 更新时间
    account_type: str = None                   # 账户类型，募集户/托管户（raising/escrow）

@dataclass
class BankAccountTransaction:
    """银行账户交易流水"""
    fund_name: str = None                      # 基金名称
    fund_code: str = None                      # 基金代码
    receive_bank_account_name: str = None      # 收款方银行账户名称
    receive_bank_account_number: str = None    # 收款方银行账号
    receive_bank_name: str = None              # 收款方开户行名称
    payment_bank_account_name: str = None      # 付款方银行账户名称
    payment_bank_account_number: str = None    # 付款方银行账号
    payment_bank_name: str = None              # 付款方开户行名称
    currency: str = None                       # 币种
    transaction_amount: float = None           # 交易金额
    transaction_time: datetime = None          # 交易时间
    transaction_direction: str = None          # 交易方向
    transaction_number: str = None             # 交易流水号
    bank_summary: str = None                   # 银行摘要
    transaction_remark: str = None             # 附言
