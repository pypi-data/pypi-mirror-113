# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import OrderNotFound


class bkex(Exchange):

    def describe(self):
        return self.deep_extend(super(bkex, self).describe(), {
            'id': 'bkex',
            'name': 'BKEX',
            'countries': ['BVI'],
            'version': 'v1',
            'rateLimit': 1000,
            'has': {
                'createMarketOrder': False,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchCurrencies': False,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchOHLCV': False,
                'fetchOrderBook': True,
                'fetchTrades': False,
            },
            'urls': {
                'api': {
                    'public': 'https://api.bkex.com/v1',
                    'private': 'https://api.bkex.com/v1/u',
                },
                'www': 'https://www.bkex.com',
                'doc': [
                    'https://github.com/bkexexchange/bkex-official-api-docs/blob/master/api_EN.md',
                ],
                'fees': 'https://www.bkex.com/help/instruction/33',
            },
            'api': {
                'public': {
                    'get': [
                        'exchangeInfo',
                        'q/depth',
                        'q/deals',
                        'q/ticker',
                        'q/ticker/price',
                        'q/kline',
                    ],
                },
                'private': {
                    'get': [
                        'trade/order/listUnfinished',
                        'trade/order/history',
                        'trade/order/unfinished/detail',
                        'trade/order/finished/detail',
                        'wallet/balance',
                        'wallet/address',
                        'wallet/withdraw',
                        'wallet/depositRecord',
                        'wallet/withdrawRecord',
                    ],
                    'post': [
                        'trade/order/create',
                        'trade/order/cancel',
                        'trade/order/batchCreate',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.0015,
                    'taker': 0.002,
                },
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetExchangeInfo(params)
        data = self.safe_value(response, 'data')
        markets = self.safe_value(data, 'pairs')
        numMarkets = len(markets)
        if numMarkets < 1:
            raise ExchangeError(self.id + ' publicGetExchangeInfo returned empty response: ' + self.json(markets))
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'pair')
            baseId = id.split('_')[0]
            quoteId = id.split('_')[1]
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'amountPrecision'),
                'price': self.safe_integer(market, 'pricePrecision') or self.safe_integer(market, 'defaultPrecision'),
            }
            minAmount = self.safe_float(market, 'minimumTradeAmount')
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': minAmount,
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        timestamp = self.milliseconds()
        market = self.market(symbol)
        request = self.extend({
            'pair': self.safe_string(market, 'id'),
        }, params)
        response = self.publicGetQTicker(request)
        ticker = self.safe_value(response, 'data')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'h'),
            'low': self.safe_float(ticker, 'l'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'previousClose': None,
            'open': self.safe_float(ticker, 'o'),
            'close': self.safe_float(ticker, 'c'),
            'last': self.safe_float(ticker, 'c'),
            'percentage': None,
            'change': self.safe_float(ticker, 'r'),
            'average': None,
            'baseVolume': self.safe_float(ticker, 'a'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        if limit is not None:
            request['size'] = limit
        response = self.publicGetQDepth(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return self.parse_order_book(data, None, 'bids', 'asks', 'price', 'amt')

    def fetch_balance(self, params={}):
        self.load_markets()
        query = self.omit(params, 'type')
        response = self.privateGetWalletBalance(query)
        balances = self.safe_value(response, 'data')
        wallets = self.safe_value(balances, 'WALLET')
        result = {'info': wallets}
        for i in range(0, len(wallets)):
            wallet = wallets[i]
            currencyId = wallet['coinType']
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(wallet, 'available')
            account['total'] = self.safe_float(wallet, 'total')
            result[code] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePostTradeOrderCreate'
        direction = side == 'BID' if 'buy' else 'ASK'
        request = {
            'amount': self.amount_to_precision(symbol, amount),
            'direction': direction,
            'pair': self.safe_string(market, 'id'),
            'price': self.price_to_precision(symbol, price),
        }
        response = getattr(self, method)(self.extend(request, params))
        return {
            'id': self.safe_value(response, 'data'),
            'info': response,
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'orderNo': id,
            'pair': self.market_id(symbol),
        }
        return self.privatePostTradeOrderCancel(self.extend(request, params))

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': self.safe_string(market, 'id'),
        }
        if limit is not None:
            request['size'] = limit
        response = self.privateGetTradeOrderListUnfinished(self.extend(request, params))
        result = self.safe_value(response, 'data')
        return self.parse_orders(self.safe_value(result, 'data'), market, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'orderNo': id,
            'pair': self.market_id(symbol),
        }
        response = self.privateGetTradeOrderUnfinishedDetail(self.extend(request, params))
        data = self.safe_value(response, 'data')
        if not data:
            raise OrderNotFound(self.id + ' order ' + id + ' not found')
        return self.parse_order(data)

    def parse_order(self, order, market=None):
        marketName = self.safe_string(order, 'pair')
        market = market or self.find_market(marketName)
        timestamp = self.safe_string(order, 'createdTime')
        if timestamp is not None:
            timestamp = int(round(float(timestamp)) * 1000)
        direction = self.safe_value(order, 'direction')
        side = direction == 'BUY' if 'BID' else 'SELL'
        amount = self.safe_float(order, 'totalAmount')
        fillAmount = self.safe_float(order, 'dealAmount', amount)
        remaining = amount - fillAmount
        return {
            'id': self.safe_string(order, 'id'),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': None,
            'symbol': self.safe_string(market, 'symbol'),
            'side': side,
            'type': self.safe_string(order, 'orderType'),
            'price': self.safe_float(order, 'price'),
            'cost': None,
            'amount': amount,
            'filled': fillAmount,
            'remaining': remaining,
            'fee': None,
            'info': order,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if method == 'GET':
            if query:
                url += '?' + self.urlencode(query)
        if api == 'private':
            self.check_required_credentials()
            query = self.urlencode(query)
            if method == 'POST':
                body = query
            secret = self.encode(self.secret)
            signature = self.hmac(query, secret, hashlib.sha256)
            headers = {
                'Cache-Control': 'no-cache',
                'Content-type': 'application/x-www-form-urlencoded',
                'X_ACCESS_KEY': self.apiKey,
                'X_SIGNATURE': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        httpCode = self.safe_integer(response, 'code', 200)
        if response is None:
            return
        if code >= 400:
            raise ExchangeError(self.id + ' HTTP Error ' + code + ' reason: ' + reason)
        if httpCode >= 400:
            message = self.safe_value(response, 'msg', '')
            raise ExchangeError(self.id + ' HTTP Error ' + httpCode + ' message: ' + message)
