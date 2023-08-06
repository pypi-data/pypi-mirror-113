import datetime
import requests
import time

from . import BasicCustodian
from ..data.fund import FundNav
from ..data.investor import InvestorInfo, InvestorShare
from ..data.transaction import InvestorTransactionApply, InvestorTransactionConfirm, DividendRecord, CarryRecord


class CiticSecurities(BasicCustodian):
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
        self.token = None
        self.token_valid_till = None

    def _get_token(self):
        """
        Resp sample:
        {
            "data": {
                "token": "eyJhbGciOiJIUzI1NiJ9.eyJuYmYiOjE1MjYzNTAyNjgsIkluc3RJZCI6NTI1LCJjaGFubmVsIjoiZ2F0ZXdheSIsImV4cCI6MTU1Nzg4NjI2OH0.LrMMNsVuMvQOh0ltWO6JXM74dtrF3ydJDmnKUgFJmuE"
            },
            "code": 0,
            "success": true
        }
        """
        if not self.token or datetime.datetime.now() >= self.token_valid_till:
            endpoint = 'v1/auth/getToken'
            url = f'{self.url}{endpoint}'
            resp = requests.get(url, headers={'consumerAuth': self.auth})
            data = self._parse_response(resp)
            if not data:
                return None

            self.token = data['token']
            self.token_valid_till = datetime.datetime.now() + datetime.timedelta(minutes=24*60-1)

        return self.token

    def _get(self, url, params, paging=True):
        token = self._get_token()
        if not token:
            return None

        if paging:
            params = {}
            params.update({'pageSize': 500})
            page = 1
            result = []
            while True:
                params.update({'pageNum': page})
                resp = requests.get(url, params=params, 
                                    headers={'consumerAuth': self.auth, 'Authorization': f'Bearer {token}'})

                data = self._parse_response(resp)
                if not data:
                    break

                result.extend(data.get('list', []))

                is_last_page = data.get('isLastPage', True)
                if is_last_page:
                    break
                else:
                    page += 1
                    time.sleep(1.5)

            return result
        else:
            resp = requests.get(url, params=params, 
                                headers={'consumerAuth': self.auth, 'Authorization': f'Bearer {token}'})
            return self._parse_response(resp)

    def _parse_response(self, resp):
        if resp is None:
            return None
            
        if resp.status_code != 200:
            print(f'Failed to get data, status_code: {resp.status_code}, resp: {resp.content}')
            return None

        result = resp.json()
        if result['code'] != 0:
            print(f'Failed to get data, code: {result["code"]}, message: {result["message"]}')
            return None

        return result['data']


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>> FUND RELATED FUNCTIONS >>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_fund_nav(self, start_date, end_date):
        """Response sample:
        TODO: add sample here
        """
        endpoint = '/v1/fa/queryFundNetValForApi'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'netBeginDate': start_date,
            'netEndDate': end_date,
        }
        fund_nav_list = self._get(url, params)
        if fund_nav_list is None:
            return None

        result = []
        for fund_nav in fund_nav_list:
            result.append(FundNav(
                fund_name=fund_nav['fundName'],
                fund_code=fund_nav['fundCode'],
                net_value=fund_nav['netAssetVal'],
                accumulated_net_value=fund_nav['totalAssetVal'],
                net_value_date=fund_nav['netDate'],
                asset_amount=fund_nav['assetNet'],
                asset_volume=fund_nav['assetShares'],
            ))

        return result

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<< FUND RELATED FUNCTIONS <<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>> INVESTOR RELATED FUNCTIONS >>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_investor_info(self, start_date=None, end_date=None):
        """Response sample:
        [
            {
                "bankAccount": null,
                "bankAccountName": null,
                "zipCode": null,
                "address": null,
                "bankOpenName": null,
                "tradeAcco": null,
                "certiType": "1",
                "custName": "测试用户姓名",
                "agencyNo": "ZX6",
                "fundAcco": "S58000566432",
                "custType": "2",
                "bankNo": null,
                "certiNo": "91440300398558281Q",
                "tel": "18088880003",
                "email": "test@citics.com"
            }
        ]
        """
        if start_date or end_date:
            print(f'Warning: dates ({start_date} and {end_date}) are discarded by investor info API in CITIC!')

        endpoint = 'v1/ta/queryCustInfoForApi'
        url = f'{self.url}{endpoint}'

        params = {}
        investor_list = self._get(url, params)
        if investor_list is None:
            return None

        result = []
        for investor in investor_list:
            result.append(InvestorInfo(
                investor_name=investor['custName'],
                investor_type=investor['custType'],
                certificate_type=investor['certiType'],
                certificate_number=investor['certiNo'],
                fund_account_number=investor['fundAcco'],
                trade_account_number=investor['tradeAcco'],
                # trade_account_open_date=investor[''],
                bank_account_name=investor['bankAccountName'],
                bank_account_number=investor['bankAccount'],
                bank_name=investor['bankOpenName'],
                phone=investor['tel'],
                email=investor['email'],
                address=investor['address'],
                postcode=investor['zipCode'],
                # agency_name=investor[''],
                agency_code=investor['agencyNo'],
            ))

        return result

    def get_investor_share(self, get_investor_with_no_share=False):
        """Response sample:
        [
            {
                "realShares": "10000000",
                "fundAcco": "S51000001945",
                "tradeAcco": "0269",
                "fundCode": "ST6027",
                "frozenShares": "0",
                "ackDate": "20181119",
                "enableShares": "10000000",
                "bonusType": "1",
                "lastNav": "20181120",
                "agencyNo": "ZX6"
            }
        ]
        """
        endpoint = 'v1/ta/ShareQueryForApi'
        url = f'{self.url}{endpoint}'

        params = {}
        investor_share_list = self._get(url, params=params)
        if investor_share_list is None:
            return None

        result = []
        for investor_share in investor_share_list:
            result.append(InvestorShare(
                # investor_name=investor_share[''],
                # investor_type=investor_share[''],
                # certificate_type=investor_share[''],
                # certificate_number=investor_share[''],
                fund_account_number=investor_share['fundAcco'],
                trade_account_number=investor_share['tradeAcco'],
                # fund_name=investor_share[''],
                fund_code=investor_share['fundCode'],
                total_share=investor_share['realShares'],
                available_share=investor_share['enableShares'],
                frozen_share=investor_share['frozenShares'],
                share_date=investor_share['ackDate'],
                # agency_name=investor_share[''],
                agency_code=investor_share['agencyNo'],
                # structured_fund_name=investor_share[''],
                # structured_fund_code=investor_share[''],
                dividend_method=investor_share['bonusType'],
            ))

        return result
        
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<< INVESTOR RELATED FUNCTIONS <<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>> TRANSACTION RELATED FUNCTIONS >>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_investor_transaction_apply(self, start_date, end_date):
        """Response sample:
        [
            {
                "tradeAcco": "0145",
                "bankName": "中信银行",
                "certiType": null,
                "dividendMethod": null,
                "requestNo": "20181106001896",
                "confirmFlag": null,
                "custName": null,
                "bankAcco": "62283000000003180",
                "shareType": "A",
                "requestTime": "091013",
                "confirmDate": null,
                "businFlag": "022",
                "balance": "55040000",
                "fundCode": "ST6027",
                "requestDate": "20181106",
                "bankNo": "001",
                "custType": null,
                "certiNo": null,
                "share": "0",
                "state": "0"
            }
        ]
        """
        endpoint = 'v1/ta/queryTradeApplyForApi'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'requestBeginDate': start_date,
            'requestEndDate': end_date,
        }

        # TODO: set log level
        # print(params)
        # return

        investor_transaction_apply_list = self._get(url, params)
        if investor_transaction_apply_list is None:
            return None

        result = []
        for investor_transaction_apply in investor_transaction_apply_list:
            result.append(InvestorTransactionApply(
                investor_name=investor_transaction_apply['custName'],
                investor_type=investor_transaction_apply['custType'],
                certificate_type=investor_transaction_apply['certiType'],
                certificate_number=investor_transaction_apply['certiNo'],
                # fund_account_number=investor_transaction_apply[''],
                trade_account_number=investor_transaction_apply['tradeAcco'],
                # fund_name=investor_transaction_apply[''],
                fund_code=investor_transaction_apply['fundCode'],
                business_type=investor_transaction_apply['businFlag'],
                apply_amount=investor_transaction_apply['balance'],
                apply_volume=investor_transaction_apply['share'],
                apply_date=investor_transaction_apply['requestDate'],
                # commission_discount=investor_transaction_apply[''],
                # agency_name=investor_transaction_apply[''],
                # agency_number=investor_transaction_apply[''],
                # structured_fund_name=investor_transaction_apply[''],
                # structured_fund_code=investor_transaction_apply[''],
            ))

        return result

    def get_investor_transaction_confirm(self, start_date, end_date, use_apply_date=True):
        """Response sample:
        [
            {
                "profitBalanceForAgency": "0",
                "tradeAcco": "0186",
                "tradeFee": "0",
                "exRequestNo": "20181119000053",
                "interestShare": "0",
                "profitBalance": "0",
                "unShares": "0",
                "adjustCause": "0",
                "backFee": "0",
                "taFlag": "0",
                "fundCode": "ST6027",
                "ackAmt": "100",
                "interest": "0",
                "subQuty": "100",
                "taFee": "0",
                "registFee": "0",
                "currency": "人民币",
                "retCod": null,
                "bonusType": null,
                "fundFee": "0",
                "apkind": "03",
                "nav": "1",
                "ackQuty": "100",
                "frozenBalance": "0",
                "ackDate": "20181120",
                "totalNav": "1",
                "unfrozenBalance": "0",
                "agencyNo": "ZX6",
                "retMsg": null,
                "agencyName": "直销",
                "ackNo": "ZX60000172284",
                "subAmt": "0",
                "ackStatus": "1",
                "fundAcco": "S51000001136",
                "totalFee": "0",
                "applyDate": "20181119",
                "largeRedemptionFlag": "1",
                "agencyFee": "0",
                "shareLevel": null,
                "interestTax": "0"
            }
        ]
        """
        endpoint = 'v1/ta/TradeConfirmationForApi'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        if use_apply_date:
            params = {
                'applyBeginDate': start_date,
                'applyEndDate': end_date,
            }
        else:
            params = {
                'ackBeginDate': start_date,
                'ackEndDate': end_date,
            }
        investor_transaction_confirm_list = self._get(url, params)
        if investor_transaction_confirm_list is None:
            return None

        result = []
        for investor_transaction_confirm in investor_transaction_confirm_list:
            result.append(InvestorTransactionConfirm(
                # investor_name=investor_transaction_confirm[''],
                # investor_type=investor_transaction_confirm[''],
                # certificate_type=investor_transaction_confirm[''],
                # certificate_number=investor_transaction_confirm[''],
                fund_account_number=investor_transaction_confirm['fundAcco'],
                trade_account_number=investor_transaction_confirm['tradeAcco'],
                # fund_name=investor_transaction_confirm[''],
                fund_code=investor_transaction_confirm['fundCode'],
                business_type=investor_transaction_confirm['apkind'],
                apply_amount=investor_transaction_confirm['subAmt'],
                apply_volume=investor_transaction_confirm['subQuty'],
                apply_date=investor_transaction_confirm['applyDate'],
                # commission_discount=investor_transaction_confirm[''],
                agency_name=investor_transaction_confirm['agencyName'],
                agency_number=investor_transaction_confirm['agencyNo'],
                # structured_fund_name=investor_transaction_confirm[''],
                # structured_fund_code=investor_transaction_confirm[''],
                net_value=investor_transaction_confirm['nav'],
                confirm_date=investor_transaction_confirm['ackDate'],
                confirm_amount=investor_transaction_confirm['ackAmt'],
                # confirm_net_amount=investor_transaction_confirm[''],
                confirm_volume=investor_transaction_confirm['ackQuty'],
                commission=investor_transaction_confirm['totalFee'],
                carry=investor_transaction_confirm['profitBalance'],
                interest=investor_transaction_confirm['interest'],
                interest_to_volume=investor_transaction_confirm['interestShare'],
                apply_number=investor_transaction_confirm['exRequestNo'],
                confirm_number=investor_transaction_confirm['ackNo'],
            ))

        return result

    def get_dividend_record(self, start_date, end_date):
        """
        [
            {
                "date": "20170602",
                "realBalance": "30013.84",
                "realShares": "0",
                "flag": "1",
                "totalProfit": "30013.84",
                "tradeAcco": "000S5095800024783",
                "netValue": "0",
                "reinvestBalance": "0",
                "cserialNo": "ZX20000036156",
                "regDate": "20170601",
                "certiType": "0",
                "custName": "测试用客户",
                "agencyNo": "ZX2",
                "unitProfit": "0.025",
                "agencyName": "私募直销2",
                "confirmDate": "20170602",
                "deductBalance": "0",
                "fundAcco": "S51000021633",
                "fundCode": "ST6027",
                "custType": "1",
                "certiNo": "330102195602231816",
                "fundName": "测试用基金",
                "totalShare": "1200000",
                "lastDate": "20170602"
            }
        ]
        """
        endpoint = 'v1/ta/queryDividendForApi'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'confirmBeginDate': start_date,
            'confirmEndDate': end_date,
        }
        dividend_record_list = self._get(url, params)
        if dividend_record_list is None:
            return None

        result = []
        for dividend_record in dividend_record_list:
            result.append(DividendRecord(
                investor_name=dividend_record['custName'],
                investor_type=dividend_record['custType'],
                certificate_type=dividend_record['certiType'],
                certificate_number=dividend_record['certiNo'],
                fund_account_number=dividend_record['fundAcco'],
                trade_account_number=dividend_record['tradeAcco'],
                fund_name=dividend_record['fundName'],
                fund_code=dividend_record['fundCode'],
                agency_name=dividend_record['agencyName'],
                agency_number=dividend_record['agencyNo'],
                confirm_date=dividend_record['confirmDate'],
                confirm_number=dividend_record['cserialNo'],
                date_of_record=dividend_record['regDate'],
                date_of_payment=dividend_record['date'],
                dividend_base_volume=dividend_record['totalShare'],
                dividend_per_share=dividend_record['unitProfit'],
                total_dividend=dividend_record['totalProfit'],
                dividend_method=dividend_record['flag'],
                dividend_cash=dividend_record['realBalance'],
                dividend_reinvest_amount=dividend_record['reinvestBalance'],
                dividend_reinvest_volume=dividend_record['realShares'],
                dividend_reinvest_date=dividend_record['lastDate'],
                dividend_reinvest_net_value=dividend_record['netValue'],
                carry=dividend_record['deductBalance'],
            ))

        return result

    def get_carry_record(self, start_date, end_date):
        """
        [
            {
                "tradeAcco": "000S5095800045565",
                "cserialNo": "ZX100000046420000000",
                "hold": "0",
                "shares": "7500000",
                "calcFlag": "0",
                "oriCserialNo": "ZX10000004530",
                "businFlag": "58",
                "shareTypeCn": "前收费",
                "fundCode": "SK2915",
                "bonusBalance": "0",
                "requestDate": "20170619",
                "currRatio": "0",
                "factShares": "0",
                "nav": "1",
                "factBalance": "0",
                "oriTotalNav": "1",
                "totalNav": "1",
                "yearRatio": "0",
                "custName": "测试用客户",
                "agencyNo": "ZX1",
                "sortFlag": "1",
                "agencyName": "私募直销",
                "endIndexPrice": "0",
                "confirmDate": "20170619",
                "beginDate": "20170619",
                "indexYearRatio": "0",
                "fundAcco": "S50000197850",
                "custType": "0",
                "oriBalance": "0",
                "fundName": "测试用基金",
                "oriNav": "1",
                "beginIndexPrice": "0",
                "registDate": "20170619"
            }
        ]
        """
        endpoint = 'v1/ta/queryTaProfitForApi'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'calcFlag': 0,      # 0-计提，1-试算
            'confirmBeginDate': start_date,
            'confirmEndDate': end_date,
        }
        carry_record_list = self._get(url, params)
        if carry_record_list is None:
            return None

        result = []
        for carry_record in carry_record_list:
            result.append(CarryRecord(
                investor_name=carry_record['custName'],
                investor_type=carry_record['custType'],
                # certificate_type=carry_record[''],
                # certificate_number=carry_record[''],
                fund_account_number=carry_record['fundAcco'],
                trade_account_number=carry_record['tradeAcco'],
                fund_name=carry_record['fundName'],
                fund_code=carry_record['fundCode'],
                agency_name=carry_record['agencyName'],
                agency_number=carry_record['agencyNo'],
                apply_date=carry_record['requestDate'],
                confirm_date=carry_record['confirmDate'],
                share_type=carry_record['shareTypeCn'],  # Chinese char
                confirm_number=carry_record['cserialNo'],
                share_register_date=carry_record['registDate'],
                share_count=carry_record['shares'],
                initial_date=carry_record['beginDate'],
                initial_net_value=carry_record['oriNav'],
                initial_accumulated_net_value=carry_record['oriTotalNav'],
                final_net_value=carry_record['nav'],
                final_accumulated_net_value=carry_record['totalNav'],
                total_return_rate=carry_record['currRatio'],
                annualized_return_rate=carry_record['yearRatio'],
                base_amount=carry_record['oriBalance'],
                actual_base_amount=carry_record['factBalance'],
                actual_base_volume=carry_record['factShares'],
                total_dividend=carry_record['bonusBalance'],
                original_confirm_number=carry_record['oriCserialNo'],
                holding_days=carry_record['hold'],
                index_annualized_return_rate=carry_record['indexYearRatio'],
                initial_index_price=carry_record['beginIndexPrice'],
                final_index_price=carry_record['endIndexPrice'],
                calculation_flag=carry_record['calcFlag'],
            ))

        return result

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<< TRANSACTION RELATED FUNCTIONS <<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


if __name__ == '__main__':
    test_url = 'https://apitest.iservice.citics.com/'
    test_auth = ''
    cs = CiticSecurities(
        url = test_url, 
        auth = test_auth, 
    )

    # Test fund nav
    start_date = datetime.datetime.today() - datetime.timedelta(days=60)
    end_date = datetime.datetime.today()
    fund_nav_list = cs.get_fund_nav(start_date, end_date)
    print(f'fund nav: {fund_nav_list}\n')

    # Test investor info
    investor_info_list = cs.get_investor_info()
    print(f'investor info: {investor_info_list}\n')

    # Test investor share
    investor_share_list = cs.get_investor_share()
    print(f'investor share: {investor_share_list}\n')

    # Test investor transaction apply
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    investor_transaction_apply_list = cs.get_investor_transaction_apply(start_date, end_date)
    print(f'investor transaction apply: {investor_transaction_apply_list}\n')

    # # Test investor transaction confirm
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    investor_transaction_confirm_list = cs.get_investor_transaction_confirm(start_date, end_date)
    print(f'investor transaction confirm: {investor_transaction_confirm_list}\n')

    # Test dividend record
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    dividend_record_list = cs.get_dividend_record(start_date, end_date)
    print(f'dividend record: {dividend_record_list}\n')

    # Test carry record
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    carry_record_list = cs.get_carry_record(start_date, end_date)
    print(f'carry record: {carry_record_list}\n')
