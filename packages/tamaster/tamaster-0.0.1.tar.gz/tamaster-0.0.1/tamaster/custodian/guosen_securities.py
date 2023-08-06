import datetime
import hashlib
import requests

from . import BasicCustodian
from ..data.fund import FundNav
from ..data.investor import InvestorInfo, InvestorShare
from ..data.transaction import InvestorTransactionApply, InvestorTransactionConfirm, DividendRecord

class GuosenSecurities(BasicCustodian):
    def __init__(self, url, manager_id, app_id, app_secret):
        self.url = url
        self.manager_id = manager_id
        self.app_id = app_id
        self.app_secret = app_secret

    def _get_sign(self, params):
        param_str = f'{self.app_secret}'
        for key in sorted(params):
            param_str += f'{key}{params[key]}'

        md5 = hashlib.md5()
        md5.update(param_str.encode())
        return md5.hexdigest().upper()

    def _parse_response(self, resp):
        if resp.status_code != 200:
            print(f'Failed to get data, status_code: {resp.status_code}, resp: {resp.content}')
            return None

        result = resp.json()
        print(result)
        if result['code'] != '200':
            print(f'Failed to get data, code: {result["code"]}, message: {result["message"]}')
            return None

        return result['returnObject']

    def _get(self, url, params):
        params.update({
            'managerCode': self.manager_id,
            'appId': self.app_id,
        })
        params['sign'] = self._get_sign(params)
        
        resp = requests.get(url, params=params)
        return self._parse_response(resp)


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>> FUND RELATED FUNCTIONS >>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_fund_nav(self, start_date, end_date, check_status=True):
        """Response sample:
        [
            {
                "checkStatus": "1",
                "fundAssets": 1234567.89,
                "fundCode": "xx",
                "fundName": "xx",
                "fundShares": 1234567.89,
                "managerName": "xx",
                "netValue": 1.0000,
                "netValueDate": "20200102",
                "netValueLength": 4,
                "totalNetValue": 1.0000
            },
            {
                "checkStatus": "1",
                "fundAssets": 1234567.89,
                "fundCode": "xx",
                "fundName": "xx",
                "fundShares": 1234567.89,
                "managerName": "xx",
                "netValue": 1.0000,
                "netValueDate": "20200101",
                "netValueLength": 4,
                "totalNetValue": 1.0000
            }
        ]
        """
        endpoint = 'netValueInfo/queryList'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'startDate': start_date,
            'endDate': end_date,
            'checkStatus': 1 if check_status else 0,
        }
        fund_nav_list = self._get(url, params=params)
        if fund_nav_list is None:
            return None

        result = []
        for fund_nav in fund_nav_list:
            result.append(FundNav(
                fund_name=fund_nav['fundName'],
                fund_code=fund_nav['fundCode'],
                net_value=fund_nav['netValue'],
                accumulated_net_value=fund_nav['totalNetValue'],
                net_value_date=fund_nav['netValueDate'],
                asset_amount=fund_nav['fundAssets'],
                asset_volume=fund_nav['fundShares'],
            ))

        return result

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<< FUND RELATED FUNCTIONS <<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>> INVESTOR RELATED FUNCTIONS >>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_investor_info(self, start_date, end_date):
        """Response sample:
        [
            {
                "accountName": "xx",
                "bankAccount": "6222x906538",
                "bankName": "中国工商银行",
                "customerName": "xx",
                "customerType": "1",
                "customerTypeName": "个人",
                "fundAccount": "Sxx0",
                "identityNo": "110xxx1635",
                "identityType": "0",
                "identityTypeName": "身份证",
                "openDate": "20180615",
                "orderTradeAccount": "gxhs0xxx",
                "tradeAccount": "gxhs01xxx"
            }
        ]
        """
        endpoint = 'investorInfo/queryList/v2'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'startOpenDate': start_date,
            'endOpenDate': end_date,
        }
        investor_list = self._get(url, params=params)
        if investor_list is None:
            return None

        result = []
        for investor in investor_list:
            result.append(InvestorInfo(
                investor_name=investor['customerName'],
                investor_type=investor['customerType'],
                certificate_type=investor['identityType'],
                certificate_number=investor['identityNo'],
                fund_account_number=investor['fundAccount'],
                trade_account_number=investor['tradeAccount'],
                trade_account_open_date=investor['openDate'],
                bank_account_name=investor['accountName'],
                bank_account_number=investor['bankAccount'],
                bank_name=investor['bankName'],
                order_trade_account_number=investor['orderTradeAccount'],
            ))

        return result

    def get_investor_share(self, get_investor_with_no_share=False):
        """Response sample:
        [
            {
                "agencyName": "管理人直销",
                "agencyNumber": "999",
                "customerName": "xx有限公司",
                "customerTypeCode": "0",
                "customerTypeName": "机构",
                "frozenShares": "0",
                "fundAccount": "xx",
                "fundCode": "xx",
                "fundName": "xx",
                "identityNumber": "xx",
                "identityTypeCode": "1",
                "identityTypeName": "营业执照",
                "realShares": "1234567.89",
                "shareDate": "20210101",
                "structuredFundCode": "xx",
                "structuredFundName": "xx",
                "tradeAccount": "xx"
            },
            {
                "agencyName": "管理人直销",
                "agencyNumber": "999",
                "customerName": "xx",
                "customerTypeCode": "1",
                "customerTypeName": "个人",
                "frozenShares": "0",
                "fundAccount": "xx",
                "fundCode": "xx",
                "fundName": "xx",
                "identityNumber": "xx",
                "identityTypeCode": "0",
                "identityTypeName": "身份证",
                "realShares": "1234567.89",
                "shareDate": "20210101",
                "structuredFundCode": "xx",
                "structuredFundName": "xx",
                "tradeAccount": "xx"
            }
        ]
        """
        endpoint = 'fundshare/queryShareDetail'
        url = f'{self.url}{endpoint}'

        params = {
            'isShowShareNull': 1 if get_investor_with_no_share else 0,
        }
        investor_share_list = self._get(url, params=params)
        if investor_share_list is None:
            return None

        result = []
        for investor_share in investor_share_list:
            result.append(InvestorShare(
                investor_name=investor_share['customerName'],
                investor_type=investor_share['customerTypeCode'],
                certificate_type=investor_share['identityTypeCode'],
                certificate_number=investor_share['identityNumber'],
                trade_account_number=investor_share['tradeAccount'],
                fund_name=investor_share['fundName'],
                fund_code=investor_share['fundCode'],
                total_share=investor_share['realShares'],
                frozen_share=investor_share['frozenShares'],
                share_date=investor_share['shareDate'],
                agency_name=investor_share['agencyName'],
                agency_code=investor_share['agencyNumber'],
                structured_fund_name=investor_share['structuredFundName'],
                structured_fund_code=investor_share['structuredFundCode'],
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
                "agencyCode": "999",
                "agencyName": "管理人直销",
                "businessTypeCode": "xx",
                "businessTypeName": "申购",
                "customerName": "袁xx",
                "fundAccont": "S21001600000",
                "fundName": "xxxxx1号私募基金",
                "identityNo": "4206000000000000",
                "identityTypeName": "身份证",
                "purchaseBalence": "2803476.31",
                "redeemShare": "3000000",
                "requestDate": "20190415",
                "tradeAccount": "gxhs0102xxxxxx"
            }
        ]
        """
        endpoint = 'requestConfirm/queryList'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'startDate': start_date,
            'endDate': end_date,
        }
        investor_transaction_apply_list = self._get(url, params=params)
        if investor_transaction_apply_list is None:
            return None

        result = []
        for investor_transaction_apply in investor_transaction_apply_list:
            result.append(InvestorTransactionApply(
                investor_name=investor_transaction_apply['customerName'],
                investor_type=investor_transaction_apply['customerType'],
                certificate_type=investor_transaction_apply['idTypeCode'],
                certificate_number=investor_transaction_apply['identityNo'],
                fund_account_number=investor_transaction_apply['fundAccont'],
                trade_account_number=investor_transaction_apply['tradeAccount'],
                fund_name=investor_transaction_apply['fundName'],
                fund_code=investor_transaction_apply['fundCode'],
                business_type=investor_transaction_apply['businessTypeCode'],
                apply_amount=investor_transaction_apply['purchaseBalence'],
                apply_volume=investor_transaction_apply['redeemShare'],
                apply_date=investor_transaction_apply['requestDate'],
                agency_name=investor_transaction_apply['agencyName'],
                agency_number=investor_transaction_apply['agencyCode'],
            ))

        return result

    def get_investor_transaction_confirm(self, start_date, end_date, use_apply_date=True):
        """Response sample:
        [
            {
                "agency": "xx正行",
                "agencyNumber": "301",
                "applyDate": "20180601",
                "businessFlag": "50",
                "businessFlagName": "基金成立",
                "charge": "0",
                "confirmDate": "20180605",
                "confirmMoney": "10000000",
                "confirmNumber": "xxx",
                "confirmShare": "10000000",
                "customerName": "陈xx",
                "customerTypeCode": "1",
                "customerTypeName": "个人",
                "fundAccount": "GS1000214xx",
                "fundCode": "SCY906",
                "fundName": "xx号私募基金",
                "idNumber": "33xxxxxxxx",
                "idType": "身份证",
                "idTypeCode": "0",
                "interest": "0",
                "interestShare": "0",
                "lastModify": "20170919",
                "managerCode": "5206",
                "netValue": "1",
                "profitBalance": "0",
                "raiseFare": "0",
                "redeemFare": "0",
                "requestBalance": "10000000",
                "requestNnumber": "201806010000000xxxx",
                "requestShare": "0",
                "serialNumber": "1",
                "subscribeFare": "0",
                "tradeAccount": "GS100xxxx",
                "tradeFare": "0"
            }
        ]
        """
        endpoint = 'taConfirmInfo/queryList'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'startDate': start_date,
            'endDate': end_date,
            'queryType': 1 if use_apply_date else 2,
        }
        investor_transaction_confirm_list = self._get(url, params=params)
        if investor_transaction_confirm_list is None:
            return None

        result = []
        for investor_transaction_confirm in investor_transaction_confirm_list:
            result.append(InvestorTransactionConfirm(
                investor_name=investor_transaction_confirm['customerName'],
                investor_type=investor_transaction_confirm['customerTypeCode'],
                certificate_type=investor_transaction_confirm['idTypeCode'],
                certificate_number=investor_transaction_confirm['idNumber'],
                fund_account_number=investor_transaction_confirm['fundAccount'],
                trade_account_number=investor_transaction_confirm['tradeAccount'],
                fund_name=investor_transaction_confirm['fundName'],
                fund_code=investor_transaction_confirm['fundCode'],
                business_type=investor_transaction_confirm['businessFlag'],
                apply_amount=investor_transaction_confirm['requestBalance'],
                apply_volume=investor_transaction_confirm['requestShare'],
                apply_date=investor_transaction_confirm['applyDate'],
                agency_name=investor_transaction_confirm['agency'],
                agency_number=investor_transaction_confirm['agencyNumber'],
                net_value=investor_transaction_confirm['netValue'],
                confirm_date=investor_transaction_confirm['confirmDate'],
                confirm_amount=investor_transaction_confirm['confirmMoney'],
                confirm_volume=investor_transaction_confirm['confirmShare'],
                commission=investor_transaction_confirm['totalFare'],
                carry=investor_transaction_confirm['profitBalance'],
                interest=investor_transaction_confirm['interest'],
                interest_to_volume=investor_transaction_confirm['interestShare'],
                apply_number=investor_transaction_confirm['requestNnumber'],
                confirm_number=investor_transaction_confirm['confirmNumber'],
            ))

        return result

    def get_dividend_record(self, start_date, end_date):
        endpoint = 'fundDividend/queryList'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'startDate': start_date,
            'endDate': end_date,
        }
        dividend_record_list = self._get(url, params=params)
        DividendRecord
        # TODO: convert dividend record 
        # for dividend_record in dividend_record_list:
        #     pass

        return dividend_record_list

    def get_carry_record(self, start_date, end_date):
        print('Warning: Carry API is not provided by Guosen!')
        return []

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<< TRANSACTION RELATED FUNCTIONS <<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

if __name__ == '__main__':
    test_url = 'http://61.142.2.99:9880/xxl/'
    test_manager_id = 0
    test_app_id = ''
    test_app_secret = ''

    gs = GuosenSecurities(
        url = test_url, 
        manager_id = test_manager_id, 
        app_id = test_app_id, 
        app_secret = test_app_secret,
    )

    # Test fund nav
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    fund_nav_list = gs.get_fund_nav(start_date, end_date)
    print(f'fund nav: {fund_nav_list}')

    # Test fund valuation
    valuation_date = datetime.datetime.today() - datetime.timedelta(days=7)
    fund_valuation_list = gs.get_fund_valuation(valuation_date)
    print(f'fund valuation: {fund_valuation_list}')

    # Test investor info
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    investor_info_list = gs.get_investor_info(start_date, end_date)
    print(f'investor info: {investor_info_list}')

    # Test investor share
    investor_share_list = gs.get_investor_share()
    print(f'investor share: {investor_share_list}')

    # Test investor transaction apply
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    investor_transaction_apply_list = gs.get_investor_transaction_apply(start_date, end_date)
    print(f'investor transaction apply: {investor_transaction_apply_list}')

    # # Test investor transaction confirm
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    investor_transaction_confirm_list = gs.get_investor_transaction_confirm(start_date, end_date)
    print(f'investor transaction confirm: {investor_transaction_confirm_list}')

    # Test dividend record
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    dividend_record_list = gs.get_dividend_record(start_date, end_date)
    print(f'dividend record: {dividend_record_list}')



