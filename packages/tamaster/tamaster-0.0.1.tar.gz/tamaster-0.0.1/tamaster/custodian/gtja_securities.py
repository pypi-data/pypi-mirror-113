import base64
import datetime
import hashlib
import hmac
import json
import pytz
import requests
import time

from . import BasicCustodian

class GtjaSecurities(BasicCustodian):
    def __init__(self, url, manager_id, app_key, app_secret):
        self.url = url
        self.manager_id = manager_id
        self.app_key = app_key
        self.app_secret = app_secret

    def _get_request_params(self, params):
        biz_param = json.dumps(params)
        req_params = {
            'appkey': self.app_key,
            'timeStamp': datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S%f')[:-3],
            'managerId': self.manager_id,
            'bizParam': biz_param,
        }
        # print(req_params)
        param_str = ''
        for key in sorted(req_params):
            param_str += f'{key}={req_params[key]}&'
        param_str = param_str[:-1]
        appsigned = base64.b64encode(
            hmac.new(
                self.app_secret.encode('utf-8'),
                param_str.encode('utf-8'),
                hashlib.sha512
            ).digest()
        )
        # print(appsigned)
        req_params.update({'appsigned': appsigned})
        return req_params

    def _get(self, url, params, paging=True):
        if paging:
            page_count = 20
            params = {}
            params.update({'reqNum': page_count})
            page = 1
            result = []
            while True:
                params.update({'reqPageno': page})
                request_params = self._get_request_params(params)
                resp = requests.get(url, params=request_params)

                data = self._parse_response(resp)
                if not data:
                    break

                result.extend(data.get('result', []))

                row_count = data.get('rowCount', 0)
                total_count = data.get('totalCount', 0)

                if page_count*(page-1) + row_count >= total_count:
                    break
                else:
                    page += 1
                    time.sleep(1.5)

            return result
        else:
            self._get_request_params(params)
            resp = requests.get(url, params=params, 
                                headers={'consumerAuth': self.auth, 'Authorization': f'Bearer {token}'})
            return self._parse_response(resp)

    def _parse_response(self, resp):
        if not resp:
            return None
            
        if resp.status_code != 200:
            print(f'Failed to get data, status_code: {resp.status_code}, resp: {resp.content}')
            return None

        print(resp.content)
        result = resp.json()
        if result['retCode'] != 0:
            print(f'Failed to get data, code: {result["retCode"]}, message: {result["retMsg"]}')
            return None

        return result['data']


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>> FUND RELATED FUNCTIONS >>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_fund_nav(self, start_date, end_date):
        endpoint = 'queryService.fundnetval'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'netDateBegin': start_date,
            'netDateEnd': end_date,
        }

        # TODO: set log level
        # print(params)
        # return

        fund_nav_list = self._get(url, params=params)

        # TODO: convert fund nav 
        # for investor in fund_nav_list:
        #     pass

        return fund_nav_list

    def get_fund_valuation(self, valuation_date, check_status=True):
        print('Warning: Fund valiation API is not provided by GTJA!')
        return []

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<< FUND RELATED FUNCTIONS <<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>> INVESTOR RELATED FUNCTIONS >>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_investor_info(self, start_date, end_date):
        endpoint = 'queryService.custinfo'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {}

        # TODO: set log level
        # print(params)
        # return

        investor_list = self._get(url, params=params)

        # TODO: convert investor 
        # for investor in investor_list:
        #     pass

        return investor_list

    def get_investor_share(self, get_investor_with_no_share=False):
        endpoint = 'queryService.shareholderinfo'
        url = f'{self.url}{endpoint}'

        params = {}

        # TODO: set log level
        # print(params)
        # return

        investor_share_list = self._get(url, params=params)

        # TODO: convert investor 
        # for investor_share in investor_share_list:
        #     pass

        return investor_share_list

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<< INVESTOR RELATED FUNCTIONS <<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>> TRANSACTION RELATED FUNCTIONS >>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_investor_transaction_apply(self, start_date, end_date):
        print('Warning: Investor transaction apply API is not provided by GTJA!')
        return []

    def get_investor_transaction_confirm(self, start_date, end_date, use_apply_date=True):
        endpoint = 'queryService.confirminfo'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        if use_apply_date:
            params = {
                'beginDate': start_date,
                'endDate': end_date,
            }
        else:
            params = {
                'confDateBegin': start_date,
                'confDateEnd': end_date,
            }

        # TODO: set log level
        # print(params)
        # return

        investor_transaction_confirm_list = self._get(url, params=params)

        # TODO: convert investor transaction confirm
        # for investor_transaction_confirm in investor_transaction_confirm_list:
        #     pass

        return investor_transaction_confirm_list

    def get_dividend_record(self, start_date, end_date):
        endpoint = 'queryService.queryBonusInfo'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'regDateBeg': start_date,
            'regDateEnd': end_date,
        }

        # TODO: set log level
        # print(params)
        # return

        dividend_record_list = self._get(url, params=params)

        # TODO: convert dividend record 
        # for dividend_record in dividend_record_list:
        #     pass

        return dividend_record_list

    def get_carry_record(self, start_date, end_date):
        endpoint = 'queryService.fundprofit'
        url = f'{self.url}{endpoint}'

        if type(start_date) is datetime.datetime:
            start_date = start_date.strftime('%Y%m%d')
        if type(end_date) is datetime.datetime:
            end_date = end_date.strftime('%Y%m%d')

        params = {
            'beginDate': start_date,
            'endDate': end_date,
        }

        # TODO: set log level
        # print(params)
        # return

        carry_record_list = self._get(url, params=params)

        # TODO: convert dividend record 
        # for carry_record in carry_record_list:
        #     pass

        return carry_record_list

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<< TRANSACTION RELATED FUNCTIONS <<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

if __name__ == '__main__':
    test_url = 'https://pbtest.gtja.com/fsdpl-api/api/'
    test_manager_id = ''
    test_app_key = ''
    test_app_secret = ''

    gs = GtjaSecurities(
        url = test_url, 
        manager_id = test_manager_id, 
        app_key = test_app_key, 
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



