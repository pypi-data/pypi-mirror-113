# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound


class tokenomy(Exchange):

    def describe(self):
        return self.deep_extend(super(tokenomy, self).describe(), {
            'id': 'tokenomy',
            'name': 'TOKENOMY',
            'countries': ['SG'],  # Singapore
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchTickers': False,
                'fetchOrder': True,
                'fetchOrders': False,
                'fetchClosedOrders': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': False,
                'fetchCurrencies': False,
                'withdraw': True,
                'fetchMarkets': True,
            },
            'version': '1.8',
            'urls': {
                'logo': 'https://camo.githubusercontent.com/b0fde0930f9bdb9b47b3abd2e31ac05418b2a051/68747470733a2f2f7777772e746f6b656e6f6d792e636f6d2f696d616765732f746f6b656e6f6d792f4c4f474f5f544f4b454e4f4d592e706e67',
                'api': {
                    'public': 'https://exchange.tokenomy.com/api',
                    'private': 'https://exchange.tokenomy.com/tapi',
                },
                'www': 'https://www.exchange.tokenomy.com',
                'doc': 'https://exchange.tokenomy.com/help/api',
                'referral': 'https://exchange.tokenomy.com/ref/201108ade331e6e0/1',
            },
            'api': {
                'public': {
                    'get': [
                        'summaries',
                        '{pair}/ticker',
                        '{pair}/trades',
                        '{pair}/depth',
                        'market_info',
                    ],
                },
                'private': {
                    'post': [
                        'getInfo',
                        'transHistory',
                        'trade',
                        'tradeHistory',
                        'getOrder',
                        'openOrders',
                        'cancelOrder',
                        'orderHistory',
                        'withdrawCoin',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0,
                    'taker': 0.0025,
                },
            },
        })

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetInfo()
        balance = response['return']
        result = {'info': balance}
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            currency = self.currencies[code]
            lowercase = currency['id']
            account = self.account()
            account['free'] = self.safe_float(balance['balance'], lowercase, 0.0)
            account['used'] = self.safe_float(balance['balance_hold'], lowercase, 0.0)
            account['total'] = self.sum(account['free'], account['used'])
            result[code] = account
        return self.parse_balance(result)

    def fetch_markets(self, params={}):
        markets = self.publicGetMarketInfo()
        return markets

    def fetch_order_book(self, symbol, limit=None, params={}):
        marketId = symbol.replace('/', '_').lower()
        orderbook = self.publicGetPairDepth(self.extend({
            'pair': marketId,
        }, params))
        return self.parse_order_book(orderbook, None, 'buy', 'sell')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketId = symbol.replace('/', '_').lower()
        response = self.publicGetPairTicker(self.extend({
            'pair': marketId,
        }, params))
        ticker = response['ticker']
        timestamp = self.safe_float(response, 'server_time') * 1000
        baseVolume = 'vol_' + market['base'].lower()
        quoteVolume = 'vol_' + market['quote'].lower()
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, baseVolume),
            'quoteVolume': self.safe_float(ticker, quoteVolume),
            'info': ticker,
        }

    def parse_trade(self, trade, market):
        timestamp = int(trade['date']) * 1000
        return {
            'id': trade['tid'],
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['type'],
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'amount'),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketId = symbol.replace('/', '_').lower()
        response = self.publicGetPairTrades(self.extend({
            'pair': marketId,
        }, params))
        return self.parse_trades(response, market, since, limit)

    def parse_order(self, order, market=None):
        side = None
        if 'type' in order:
            side = order['type']
        status = self.safe_string(order, 'status', 'open')
        if status == 'filled':
            status = 'closed'
        elif status == 'calcelled':
            status = 'canceled'
        symbol = None
        cost = None
        price = self.safe_float(order, 'price')
        amount = None
        remaining = None
        filled = None
        if market is not None:
            symbol = market['symbol']
            quoteId = market['quoteId']
            baseId = market['baseId']
            if (market['quoteId'] == 'idr') and ('order_rp' in order):
                quoteId = 'rp'
            if (market['baseId'] == 'idr') and ('remain_rp' in order):
                baseId = 'rp'
            cost = self.safe_float(order, 'order_' + quoteId)
            if cost:
                amount = cost / price
                remainingCost = self.safe_float(order, 'remain_' + quoteId)
                if remainingCost is not None:
                    remaining = remainingCost / price
                    filled = amount - remaining
            else:
                amount = self.safe_float(order, 'order_' + baseId)
                cost = price * amount
                remaining = self.safe_float(order, 'remain_' + baseId)
                filled = amount - remaining
        average = None
        if filled:
            average = cost / filled
        timestamp = int(order['submit_time']) * 1000
        fee = None
        result = {
            'info': order,
            'id': order['order_id'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': cost,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
        }
        return result

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrder requires a symbol')
        self.load_markets()
        market = self.market(symbol)
        marketId = symbol.replace('/', '_').lower()
        response = self.privatePostGetOrder(self.extend({
            'pair': marketId,
            'order_id': id,
        }, params))
        orders = response['return']
        order = self.parse_order(self.extend({'id': id}, orders['order']), market)
        return self.extend({'info': response}, order)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        marketId = ''
        if symbol is not None:
            marketId = symbol.replace('/', '_').lower()
            market = self.market(symbol)
            request['pair'] = marketId
        response = self.privatePostOpenOrders(self.extend(request, params))
        rawOrders = None
        if marketId != '':
            rawOrders = response['return']['orders'][marketId]
        else:
            rawOrders = response['return']['orders']
        # {success: 1, return: {orders: null}} if no orders
        if not rawOrders:
            return []
        # {success: 1, return: {orders: [... objects]}} for orders fetched by symbol
        if symbol is not None:
            return self.parse_orders(rawOrders, market, since, limit)
        # {success: 1, return: {orders: {marketid: [... objects]}}} if all orders are fetched
        marketIds = list(rawOrders.keys())
        exchangeOrders = []
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            marketOrders = rawOrders[marketId]
            market = self.markets_by_id[marketId]
            parsedOrders = self.parse_orders(marketOrders, market, since, limit)
            exchangeOrders = self.array_concat(exchangeOrders, parsedOrders)
        return exchangeOrders

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol')
        self.load_markets()
        request = {}
        market = None
        marketId = ''
        if symbol is not None:
            marketId = symbol.replace('/', '_').lower()
            market = self.market(symbol)
            request['pair'] = marketId
        response = self.privatePostOrderHistory(self.extend(request, params))
        orders = self.parse_orders(response['return']['orders'], market, since, limit)
        orders = self.filter_by(orders, 'status', 'closed')
        if symbol is not None:
            return self.filter_by_symbol(orders, symbol)
        return orders

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        market = self.market(symbol)
        order = {
            'pair': symbol.replace('/', '_').lower(),
            'type': side,
            'price': price,
        }
        currency = market['base'].lower()
        if side != 'buy':
            order[currency] = amount
        order[currency] = amount
        result = self.privatePostTrade(self.extend(order, params))
        return {
            'info': result,
            'id': str(result['order_id']),
        }

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        side = self.safe_value(params, 'side')
        if side is None:
            raise ExchangeError(self.id + ' cancelOrder requires an extra "side" param')
        self.load_markets()
        return self.privatePostCancelOrder(self.extend({
            'order_id': id,
            'pair': symbol.replace('/', '_').lower(),
            'type': params['side'],
        }, params))

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        # Custom string you need to provide to identify each withdrawal.
        # Will be passed to callback URL(assigned via website to the API key)
        # so your system can identify the request and confirm it.
        # Alphanumeric, max length 255.
        requestId = self.milliseconds()
        # Alternatively:
        # requestId = self.uuid()
        request = {
            'currency': currency['id'].lower(),
            'withdraw_amount': amount,
            'withdraw_address': address,
            'request_id': str(requestId),
        }
        if tag:
            request['withdraw_memo'] = tag
        response = self.privatePostWithdrawCoin(self.extend(request, params))
        #
        #     {
        #         "success": 1,
        #         "status": "approved",
        #         "withdraw_currency": "xrp",
        #         "withdraw_address": "rwWr7KUZ3ZFwzgaDGjKBysADByzxvohQ3C",
        #         "withdraw_amount": "10000.00000000",
        #         "fee": "2.00000000",
        #         "amount_after_fee": "9998.00000000",
        #         "submit_time": "1509469200",
        #         "withdraw_id": "xrp-12345",
        #         "txid": "",
        #         "withdraw_memo": "123123"
        #     }
        #
        id = None
        if ('txid' in response) and (len(response['txid']) > 0):
            id = response['txid']
        return {
            'info': response,
            'id': id,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            url += '/' + self.implode_params(path, params)
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend({
                'method': path,
                'nonce': self.nonce() * 1000,
            }, params))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not isinstance(body, basestring):
            return
        # {success: 0, error: "invalid order."}
        # or
        # [{data, ...}, {...}, ...]
        if response is None:
            if body[0] == '{' or body[0] == '[':
                response = json.loads(body)
        if isinstance(response, list):
            return  # public endpoints may return []-arrays
        if not ('success' in response):
            return  # no 'success' property on public responses
        if response['success'] == 1:
            # {success: 1, return: {orders: []}}
            if not ('return' in response):
                if response['order_id'] is not None or response['status'] is not None:
                    return
                else:
                    raise ExchangeError(self.id + ': malformed response: ' + self.json(response))
            else:
                return
        message = response['error']
        feedback = self.id + ' ' + self.json(response)
        if message == 'Insufficient balance.':
            raise InsufficientFunds(feedback)
        elif message == 'invalid order.':
            raise OrderNotFound(feedback)  # cancelOrder(1)
        elif message.find('Minimum price ') >= 0:
            raise InvalidOrder(feedback)  # price < limits.price.min, on createLimitBuyOrder('ETH/BTC', 1, 0)
        elif message.find('Minimum order ') >= 0:
            raise InvalidOrder(feedback)  # cost < limits.cost.min on createLimitBuyOrder('ETH/BTC', 0, 1)
        elif message == 'Invalid credentials. API not found or session has expired.':
            raise AuthenticationError(feedback)  # on bad apiKey
        elif message == 'Invalid credentials. Bad sign.':
            raise AuthenticationError(feedback)  # on bad secret
        raise ExchangeError(self.id + ': unknown error: ' + self.json(response))
