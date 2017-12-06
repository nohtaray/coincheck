import time
import hmac
import hashlib
import requests
import simplejson as json
from coincheck.utils import make_header, nounce

"""
document: https://coincheck.com/documents/exchange/api
"""
class Order(object):

    def __init__(self,
                 access_key=None,
                 secret_key=None):
        self.access_key = access_key
        self.secret_key = secret_key


    def create(self,pair, order_type, rate=None, amount=None, market_buy_amount=None):
        ''' create new order function
        :param pair: str; set 'btc_jpy'
        :param order_type: str; set 'buy' or 'sell'
        :param rate: float
        :param amount: float
        :param market_buy_amount: float; Market buy amount in JPY not BTC. ex) 10000
        '''
        nonce = nounce()
        payload = { 'rate': rate,
                    'amount': amount,
                    'order_type': order_type,
                    'pair': pair,
                    'market_buy_amount': market_buy_amount
                    }
        url= 'https://coincheck.com/api/exchange/orders'
        body = 'rate={rate}&amount={amount}&order_type={order_type}&pair={pair}&market_buy_amount={market_buy_amount}'.format(**payload)
        message = nonce + url + body
        signature = hmac.new(self.secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
           'ACCESS-KEY'      : self.access_key,
           'ACCESS-NONCE'    : nonce,
           'ACCESS-SIGNATURE': signature
        }
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
