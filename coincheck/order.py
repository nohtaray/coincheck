import requests
import simplejson as json

from coincheck.utils import make_header, make_body

"""
document: https://coincheck.com/documents/exchange/api
"""
class Order(object):

    def __init__(self,
                 access_key=None,
                 secret_key=None):
        self.access_key = access_key
        self.secret_key = secret_key


    def create(self,pair, order_type, rate=None, amount=None, market_buy_amount=None, position_id=None):
        ''' create new order function
        :param pair: str; set 'btc_jpy'
        :param order_type: str; set 'buy' or 'sell'
        :param rate: float
        :param amount: float
        :param market_buy_amount: float; Market buy amount in JPY not BTC. ex) 10000
        :param position_id: int
        '''
        payload = { 'rate': rate,
                    'amount': amount,
                    'order_type': order_type,
                    'pair': pair,
                    'market_buy_amount': market_buy_amount,
                    'position_id': position_id,
                    }
        url= 'https://coincheck.com/api/exchange/orders'
        body = make_body(**payload)
        headers = make_header(url,body=body, access_key=self.access_key,secret_key=self.secret_key)
        r = requests.post(url,headers=headers,data=body)
        return json.loads(r.text)

    def buy_btc_jpy(self, **kwargs):
        return self.create(order_type='buy', pair='btc_jpy',**kwargs)

    def sell_btc_jpy(self, **kwargs):
        return self.create(order_type='sell', pair='btc_jpy',**kwargs)

    def market_buy_btc_jpy(self, jpy_amount):
        '''
        :param jpy_amount: float; Market buy amount in JPY not BTC. ex) 10000
        :return:
        '''
        return self.create(order_type='market_buy', pair='btc_jpy', market_buy_amount=jpy_amount)

    def market_sell_btc_jpy(self, amount):
        '''
        :param amount: float; Order amount. ex) 0.1
        :return:
        '''
        return self.create(order_type='market_sell', pair='btc_jpy', amount=amount)

    def leverage_buy(self, amount, rate=None):
        return self.create(order_type='leverage_buy', pair='btc_jpy', amount=amount, rate=rate)

    def leverage_sell(self, amount, rate=None):
        return self.create(order_type='leverage_sell', pair='btc_jpy', amount=amount, rate=rate)

    def close_long(self, position_id, amount, rate=None):
        return self.create(order_type='close_long', pair='btc_jpy', position_id=position_id, amount=amount, rate=rate)

    def close_short(self, position_id, amount, rate=None):
        return self.create(order_type='close_short', pair='btc_jpy', position_id=position_id, amount=amount, rate=rate)

    def list(self):
        ''' list all open orders func
        '''
        url= 'https://coincheck.com/api/exchange/orders/opens'
        headers = make_header(url,access_key=self.access_key,secret_key=self.secret_key)
        r = requests.get(url,headers=headers)
        return json.loads(r.text)

    def cancel(self,order_id):
        ''' cancel the specified order
        :param order_id: order_id to be canceled
        '''
        url= 'https://coincheck.com/api/exchange/orders/' + order_id
        headers = make_header(url,access_key=self.access_key,secret_key=self.secret_key)
        r = requests.delete(url,headers=headers)
        return json.loads(r.text)

    def history(self):
        ''' show payment history
        '''
        url= 'https://coincheck.com/api/exchange/orders/transactions'
        headers = make_header(url,access_key=self.access_key,secret_key=self.secret_key)
        r = requests.get(url,headers=headers)
        return json.loads(r.text)

    def leverage_positions(self, status):
        ''' show leverage positions
        :param status: str; 'open' or 'closed'
        '''
        url= 'https://coincheck.com/api/exchange/leverage/positions?status=' + status
        headers = make_header(url,access_key=self.access_key,secret_key=self.secret_key)
        r = requests.get(url,headers=headers)
        return json.loads(r.text)
