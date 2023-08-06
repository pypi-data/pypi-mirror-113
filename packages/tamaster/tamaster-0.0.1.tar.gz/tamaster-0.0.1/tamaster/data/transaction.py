from dataclasses import dataclass
from datetime import date

@dataclass
class InvestorTransactionApply:
    """投资者交易申请"""
    investor_name: str = None                  # 投资者名称
    investor_type: str = None                  # 投资者类型
    certificate_type: str = None               # 投资者证件类型
    certificate_number: str = None             # 投资者证件号码
    fund_account_number: str = None            # 基金账号
    trade_account_number: str = None           # 交易账号
    fund_name: str = None                      # 基金名称
    fund_code: str = None                      # 基金代码
    business_type: str = None                  # 业务类型
    apply_amount: float = None                 # 申请金额
    apply_volume: float = None                 # 申请份额
    apply_date: date = None                    # 申请日期
    commission_discount: float = None          # 手续费折扣率
    agency_name: str = None                    # 销售商名称
    agency_number: str = None                  # 销售商代码
    structured_fund_name: str = None           # 分级基金名称
    structured_fund_code: str = None           # 分级基金代码

@dataclass
class InvestorTransactionConfirm:
    """投资者交易确认"""
    investor_name: str = None                  # 投资者名称
    investor_type: str = None                  # 投资者类型
    certificate_type: str = None               # 投资者证件类型
    certificate_number: str = None             # 投资者证件号码
    fund_account_number: str = None            # 基金账号
    trade_account_number: str = None           # 交易账号
    fund_name: str = None                      # 基金名称
    fund_code: str = None                      # 基金代码
    business_type: str = None                  # 业务类型
    apply_amount: float = None                 # 申请金额
    apply_volume: float = None                 # 申请份额
    apply_date: date = None                    # 申请日期
    commission_discount: float = None          # 手续费折扣率
    agency_name: str = None                    # 销售商名称
    agency_number: str = None                  # 销售商代码
    structured_fund_name: str = None           # 分级基金名称
    structured_fund_code: str = None           # 分级基金代码
    net_value: float = None                    # 单位净值
    confirm_date: date = None                  # 确认日期
    confirm_amount: float = None               # 确认金额
    confirm_net_amount: float = None           # 确认净额
    confirm_volume: float = None               # 确认份额
    commission: float = None                   # 手续费
    carry: float = None                        # 业绩报酬
    interest: float = None                     # 利息
    interest_to_volume: float = None           # 利息转份额
    apply_number: str = None                   # 申请单编号
    confirm_number: str = None                 # 确认单编号

@dataclass
class DividendRecord:
    """分红记录"""
    investor_name: str = None                  # 投资者名称
    investor_type: str = None                  # 投资者类型
    certificate_type: str = None               # 投资者证件类型
    certificate_number: str = None             # 投资者证件号码
    fund_account_number: str = None            # 基金账号
    trade_account_number: str = None           # 交易账号
    fund_name: str = None                      # 基金名称
    fund_code: str = None                      # 基金代码
    agency_name: str = None                    # 销售商名称
    agency_number: str = None                  # 销售商代码
    confirm_date: date = None                  # 确认日期
    confirm_number: str = None                 # TA确认号
    date_of_record: date = None                # 分红登记日期
    date_of_payment: date = None               # 红利发放日期
    dividend_base_volume: float = None         # 分红基数份额
    dividend_per_share: float = None           # 每单位分红
    total_dividend: float = None               # 红利总额
    dividend_method: str = None                # 分红方式
    dividend_cash: float = None                # 实发现金红利
    dividend_reinvest_amount: float = None     # 再投资红利金额
    dividend_reinvest_volume: float = None     # 再投资份额
    dividend_reinvest_date: date = None        # 再投资日期
    dividend_reinvest_net_value: float = None  # 再投资单位净值
    carry: float = None                        # 实际业绩提成金额

@dataclass
class CarryRecord:
    """业绩报酬计提记录"""
    investor_name: str = None                  # 投资者名称
    investor_type: str = None                  # 投资者类型
    certificate_type: str = None               # 投资者证件类型
    certificate_number: str = None             # 投资者证件号码
    fund_account_number: str = None            # 基金账号
    trade_account_number: str = None           # 交易账号
    fund_name: str = None                      # 基金名称
    fund_code: str = None                      # 基金代码
    agency_name: str = None                    # 销售商名称
    agency_number: str = None                  # 销售商代码
    apply_date: date = None                    # 申请日期
    confirm_date: date = None                  # 确认日期
    share_type: date = None                    # 份额类别
    confirm_number: str = None                 # TA确认号
    share_register_date: date = None           # 份额注册日期
    share_count: float = None                  # 发生份额
    initial_date: date = None                  # 期初日期
    initial_net_value: float = None            # 期初单位净值
    initial_accumulated_net_value: float = None# 期初累计净值
    final_net_value: float = None              # 期末单位净值
    final_accumulated_net_value: float = None  # 期末累计净值
    total_return_rate: float = None            # 当前收益率
    annualized_return_rate: float = None       # 年化收益率
    base_amount: float = None                  # 应提成/保底金额
    actual_base_amount: float = None           # 实际提成/保底金额
    actual_base_volume: float = None           # 实际提成/保底金额
    total_dividend: float = None               # 分红总金额
    original_confirm_number: str = None        # 原确认单号
    holding_days: int = None                   # 持有天数
    index_annualized_return_rate: float = None # 证券指数年化收益率
    initial_index_price: float = None          # 期初指数价格
    final_index_price: float = None            # 期末指数价格
    calculation_flag: str = None               # 试算标识
