import requests
import simplejson as json

"""
document: https://coincheck.com/documents/exchange/api
"""

base_url = "https://coincheck.com"
api_urls = { 'ticker'     : '/api/ticker',
             'trades'     : '/api/trades',
             'order_books': '/api/order_books',
             'orders_rate': '/api/exchange/orders/rate'
             }

class Market(object):
    def __init__(self):
        pass


    def public_api(self, url, **kwargs):
        ''' template function of public api'''
        try :
            return json.loads(requests.get(base_url + api_urls.get(url), params=kwargs).text)
        except Exception as e:
            print(e)
    
    def ticker(self):
        '''get latest information of coincheck market'''
        return self.public_api('ticker') 
    
    def trades(self):
        '''get latest deal history of coincheck market'''
        return self.public_api('trades') 
    
    def orderbooks(self):
        '''get latest asks/bids information of coincheck market'''
        return self.public_api('order_books') 

    def orders_rate(self, order_type, pair, **kwargs):
        return self.public_api('orders_rate', order_type=order_type, pair=pair, **kwargs)


if __name__ == '__main__':
    pass
