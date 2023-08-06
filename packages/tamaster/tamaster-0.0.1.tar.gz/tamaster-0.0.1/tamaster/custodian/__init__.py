
class BasicCustodian(object):
    """Basic class of custodian API"""

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>> FUND RELATED FUNCTIONS >>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_fund_nav(self, start_date, end_date):
        raise NotImplementedError('Invalid function call of basic custodian class')

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<< FUND RELATED FUNCTIONS <<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>> INVESTOR RELATED FUNCTIONS >>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_investor_info(self, start_date, end_date):
        raise NotImplementedError('Invalid function call of basic custodian class')

    def get_investor_share(self, get_investor_with_no_share=False):
        raise NotImplementedError('Invalid function call of basic custodian class')

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<< INVESTOR RELATED FUNCTIONS <<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>> TRANSACTION RELATED FUNCTIONS >>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def get_investor_transaction_apply(self, start_date, end_date):
        raise NotImplementedError('Invalid function call of basic custodian class')

    def get_investor_transaction_confirm(self, start_date, end_date, use_apply_date=True):
        raise NotImplementedError('Invalid function call of basic custodian class')

    def get_dividend_record(self, start_date, end_date):
        raise NotImplementedError('Invalid function call of basic custodian class')

    def get_carry_record(self, start_date, end_date):
        raise NotImplementedError('Invalid function call of basic custodian class')

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<< TRANSACTION RELATED FUNCTIONS <<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
