# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DuplicateOrderId
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import TICK_SIZE


class nominex(Exchange):

    def describe(self):
        return self.deep_extend(super(nominex, self).describe(), {
            'id': 'nominex',
            'name': 'Nominex',
            'countries': ['SC'],
            'rateLimit': 1500,
            'certified': False,
            'pro': False,
            'has': {
                'CORS': False,
                'fetchCurrencies': True,
                'fetchOHLCV': True,
                'cancelAllOrders': False,
                'createDepositAddress': True,
                'deposit': False,
                'fetchClosedOrders': True,
                'fetchDepositAddress': True,
                'fetchTradingFees': True,
                'fetchMyTrades': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchTickers': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': 'TF1M',
                '5m': 'TF5M',
                '15m': 'TF15M',
                '30m': 'TF30M',
                '1h': 'TF1H',
                '3h': 'TF3H',
                '6h': 'TF6H',
                '12h': 'TF12H',
                '1d': 'TF1D',
                '1w': 'TF7D',
                '2w': 'TF14D',
                '1M': 'TF1MO',
            },
            'urls': {
                'logo': 'https://nominex.io/media/nominex-logo.png',
                'api': {
                    'public': 'https://nominex.io/api/rest/v1',
                    'private': 'https://nominex.io/api/rest/v1/private',
                },
                'demo': {
                    'public': 'https://demo.nominex.io/api/rest/v1',
                    'private': 'https://demo.nominex.io/api/rest/v1/private',
                },
                'www': 'https://nominex.io',
                'doc': [
                    'https://developer.nominex.io/',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'currencies',
                        'pairs',
                        'ticker/{symbol}',
                        'ticker',
                        'orderbook/{symbol}/A0/{limit}',
                        'candles/{symbol}/{timeframe}',
                        'trades/{symbol}',
                    ],
                },
                'private': {
                    'get': [
                        'trading-fee-rates',
                        'deposits',
                        'withdrawals',
                        'orders',
                        'orders/{id}',
                        'orders/{symbol}',
                        'trades/{symbol}',
                        'wallets',
                        'wallets/{currency}/address',
                        'wallets/{currency}/deposits',
                        'wallets/{currency}/withdrawals',
                    ],
                    'post': [
                        'orders',
                        'wallets/{currency}/address',
                        'withdrawals/{currency}',
                    ],
                    'put': [
                        'orders/{id}',
                    ],
                    'delete': [
                        'orders/{id}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                },
                'funding': {
                    'tierBased': False,  # True for tier-based/progressive
                },
            },
            'exceptions': {
                '100.2': BadSymbol,
                '101': InvalidNonce,
                '103': AuthenticationError,
                '103.4': InvalidOrder,
                '104.4': InvalidOrder,
                '110.110': RateLimitExceeded,
                '121': PermissionDenied,
                '601': BadRequest,
                '1101': InsufficientFunds,
                '1102': DuplicateOrderId,
                '1106': OrderNotFound,
                '20002': InvalidAddress,
            },
            'precisionMode': TICK_SIZE,
            'options': {
                'tradeSides': {
                    'buy': 'BUY',
                    'sell': 'SELL',
                },
                'paths': {
                    'public': '/api/rest/v1',
                    'private': '/api/rest/v1/private',
                },
            },
        })

    def fetch_trading_fees(self, params={}):
        self.load_markets()
        response = self.privateGetTradingFeeRates(params)
        return {
            'info': response,
            'maker': self.safe_float(response, 'makerFeeFactor') * 100.0,
            'taker': self.safe_float(response, 'takerFeeFactor') * 100.0,
        }

    def fetch_currencies(self, params={}):
        currencies = self.publicGetCurrencies(params)
        result = {}
        for i in range(0, len(currencies)):
            currency = self.parse_currency(currencies[i])
            currencyCode = self.safe_string(currency, 'code')
            result[currencyCode] = currency
        return result

    def parse_currency(self, currency):
        code = self.safe_string(currency, 'code')
        return {
            'id': code,
            'code': code,
            'name': self.safe_string(currency, 'name'),
            'active': True,
            'fee': self.safe_float(currency, 'withdrawalFee'),
            'precision': self.safe_integer(currency, 'scale'),
            'info': currency,
        }

    def fetch_markets(self, params={}):
        pairs = self.publicGetPairs(params)
        result = []
        for i in range(0, len(pairs)):
            market = pairs[i]
            id = self.safe_string(market, 'name')
            parts = id.split('/')
            baseId = parts[0]
            quoteId = parts[1]
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'price': self.safe_float(market, 'quoteStep'),
                'amount': self.safe_float(market, 'baseStep'),
            }
            limits = {
                'amount': {
                    'min': self.safe_float(market, 'minBaseAmount'),
                    'max': self.safe_float(market, 'maxBaseAmount'),
                },
                'cost': {
                    'min': self.safe_float(market, 'minQuoteAmount'),
                    'max': self.safe_float(market, 'maxQuoteAmount'),
                },
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': self.safe_value(market, 'active'),
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        balanceType = self.safe_string(params, 'type', 'SPOT')
        query = self.omit(params, 'type')
        response = self.privateGetWallets(query)
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            if balance['type'] == balanceType:
                currencyId = self.safe_string(balance, 'currency')
                code = self.safe_currency_code(currencyId)
                if not (code in result):
                    account = self.account()
                    account['free'] = self.safe_float(balance, 'balanceAvailable')
                    account['total'] = self.safe_float(balance, 'balance')
                    result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
            'limit': 100,
        }
        if limit == 25:
            request['limit'] = limit
        response = self.publicGetOrderbookSymbolA0Limit(self.extend(request, params))
        asks = []
        bids = []
        for i in range(0, len(response)):
            priceLevel = response[i]
            side = self.safe_string(priceLevel, 'side')
            if side == 'SELL':
                asks.append(priceLevel)
            else:
                bids.append(priceLevel)
        return self.parse_order_book({'asks': asks, 'bids': bids}, None, 'bids', 'asks', 'price', 'amount')

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        urlParams = {}
        request = {'urlParams': urlParams}
        ids = list(self.markets.keys())
        if symbols is not None:
            for i in range(0, len(symbols)):
                symbol = symbols[i]
                market = self.market(symbol)
                ids.append(market['id'])
        urlParams['pairs'] = ','.join(ids)
        response = self.publicGetTicker(self.extend(request, params))
        result = {}
        for i in range(0, len(response)):
            marketId = ids[i]
            market = self.markets[marketId]
            ticker = self.parse_ticker(response[i], market)
            symbol = market['symbol']
            result[symbol] = ticker
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        ticker = self.publicGetTickerSymbol(self.extend(request, params))
        return self.parse_ticker(ticker, market)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_integer(ticker, 'timestamp')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        elif 'pair' in ticker:
            marketId = self.safe_string(ticker, 'pair')
            if marketId is not None:
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
                    symbol = market['symbol']
                else:
                    baseId = marketId[0:3]
                    quoteId = marketId[3:6]
                    base = self.safe_currency_code(baseId)
                    quote = self.safe_currency_code(quoteId)
                    symbol = base + '/' + quote
        last = self.safe_float(ticker, 'price')
        change = self.safe_float(ticker, 'dailyChange')
        open = None
        average = None
        if last is not None and change is not None:
            open = last - change
            average = (open + last) / 2
        volume = self.safe_float(ticker, 'baseVolume')
        quoteVolume = self.safe_float(ticker, 'quoteVolume')
        vwap = (quoteVolume / volume) if (quoteVolume is not None and volume is not None and volume != 0) else None
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': self.safe_float(ticker, 'bidSize'),
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': self.safe_float(ticker, 'askSize'),
            'vwap': vwap,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': self.safe_float(ticker, 'dailyChangeP'),
            'average': average,
            'baseVolume': volume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            self.safe_integer(ohlcv, 'timestamp'),
            self.safe_float(ohlcv, 'open'),
            self.safe_float(ohlcv, 'high'),
            self.safe_float(ohlcv, 'low'),
            self.safe_float(ohlcv, 'close'),
            self.safe_float(ohlcv, 'volume'),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        if limit is None:
            limit = 100
        market = self.market(symbol)
        urlParams = {
            'limit': limit,
            'end': self.milliseconds(),
        }
        request = {
            'symbol': market['id'],
            'timeframe': self.timeframes[timeframe],
            'urlParams': urlParams,
        }
        if since is not None:
            request['start'] = since
        response = self.publicGetCandlesSymbolTimeframe(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_trade(self, trade, market):
        id = self.safe_string(trade, 'id')
        timestamp = self.safe_integer(trade, 'timestamp')
        type = None
        side = self.safe_string_lower(trade, 'side').lower()
        orderId = None
        if 'orderId' in trade:
            orderId = self.safe_string(trade, 'orderId')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        takerOrMaker = None
        if 'maker' in trade:
            maker = self.safe_value(trade, 'maker')
            takerOrMaker = 'maker' if maker else 'taker'
        feeAmount = self.safe_float(trade, 'fee')
        fee = feeAmount is None if None else {
            'cost': feeAmount,
            'currency': self.safe_string(trade, 'feeCurrencyCode'),
        }
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': type,
            'order': orderId,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=50, params={}):
        self.load_markets()
        market = self.market(symbol)
        urlParams = {}
        request = {
            'symbol': market['id'],
            'urlParams': urlParams,
        }
        if since is not None:
            urlParams['start'] = int(since)
        if limit is not None:
            urlParams['limit'] = limit
        response = self.publicGetTradesSymbol(self.extend(request, params))
        return self.parse_trades(self.safe_value(response, 'items'), market, since, limit)

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        rate = market[takerOrMaker]
        cost = amount * rate
        key = 'quote'
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
        code = market[key]
        currency = self.safe_value(self.currencies, code)
        if currency is not None:
            precision = self.safe_integer(currency, 'precision')
            if precision is not None:
                cost = float(self.currency_to_precision(code, cost))
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': cost,
        }

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a `symbol` argument')
        self.load_markets()
        market = self.market(symbol)
        urlParams = {}
        request = {
            'symbol': market['id'],
            'urlParams': urlParams,
        }
        if limit is not None:
            urlParams['limit'] = limit
        if since is not None:
            urlParams['start'] = int(since)
        response = self.privateGetTradesSymbol(self.extend(request, params))
        return self.parse_trades(self.safe_value(response, 'items'), market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        marketId = self.market_id(symbol)
        request = {
            'pairName': marketId,
            'side': self.safe_string(self.options['tradeSides'], side, side),
            'amount': self.amount_to_precision(symbol, amount),
            'type': self.upper(type),
            'walletType': self.safe_string(params, 'walletType', 'SPOT'),
        }
        if 'clientOrderId' in params:
            request['cid'] = self.safe_integer(params, 'clientOrderId')
        if type == 'limit':
            request['limitPrice'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrders(self.extend(request, params))
        return self.parse_order(response)

    def edit_order(self, id, symbol, type, side, amount=None, price=None, params={}):
        self.load_markets()
        request = {
            'walletType': self.safe_string(params, 'walletType', 'SPOT'),
        }
        if id is not None:
            request['id'] = id
        elif 'clientOrderId' in params:
            request['id'] = self.safe_integer(params, 'clientOrderId')
            request['urlParams'] = {'cid': True}
        if price is not None:
            request['limitPrice'] = self.price_to_precision(symbol, price)
        if amount is not None:
            request['amount'] = self.amount_to_precision(symbol, amount)
        if symbol is not None:
            request['pairName'] = self.market_id(symbol)
        if side is not None:
            request['side'] = self.safe_string(self.options['tradeSides'], side, side)
        if type is not None:
            request['type'] = self.upper(type)
        response = self.privatePutOrdersId(self.extend(request, params))
        return self.parse_order(response)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {}
        if id is not None:
            request['id'] = int(id)
        elif 'clientOrderId' in params:
            request['id'] = self.safe_integer(params, 'clientOrderId')
            request['urlParams'] = {'cid': True}
        return self.privateDeleteOrdersId(self.extend(request, params))

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {}
        if id is not None:
            request['id'] = int(id)
        elif 'clientOrderId' in params:
            request['id'] = self.safe_integer(params, 'clientOrderId')
            request['urlParams'] = {'cid': True}
        response = self.privateGetOrdersId(self.extend(request, params))
        return self.parse_order(response)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        if symbol is not None:
            if not (symbol in self.markets):
                raise ExchangeError(self.id + ' has no symbol ' + symbol)
        urlParams = {}
        request = {'urlParams': urlParams}
        if since is not None:
            urlParams['start'] = since
        if limit is not None:
            urlParams['limit'] = limit
        urlParams['active'] = True
        response = None
        if symbol is not None:
            marketId = self.market_id(symbol)
            request['symbol'] = marketId
            response = self.privateGetOrdersSymbol(self.extend(request, params))
        else:
            response = self.privateGetOrders(self.extend(request, params))
        return self.parse_orders(self.safe_value(response, 'items'), None, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        urlParams = {}
        request = {'urlParams': urlParams}
        if since is not None:
            urlParams['start'] = since
        if limit is not None:
            urlParams['limit'] = limit
        urlParams['active'] = False
        response = None
        if symbol is not None:
            marketId = self.market_id(symbol)
            request['symbol'] = marketId
            response = self.privateGetOrdersSymbol(self.extend(request, params))
        else:
            response = self.privateGetOrders(self.extend(request, params))
        return self.parse_orders(self.safe_value(response, 'items'), None, since, limit)

    def parse_order(self, order, market=None):
        side = self.safe_string_lower(order, 'side')
        open = self.safe_value(order, 'active')
        status = None
        if open:
            status = 'open'
        else:
            status = 'closed'
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'pairName')
            if marketId is not None:
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        orderType = self.safe_string_lower(order, 'type')
        timestamp = self.safe_integer(order, 'created')
        id = self.safe_string(order, 'id')
        lastTradeTimestamp = None
        if order.amount < order.originalAmount:
            lastTradeTimestamp = timestamp
        originalAmount = self.safe_float(order, 'originalAmount')
        amount = self.safe_float(order, 'amount')
        filled = originalAmount - amount
        resultOrder = {
            'info': order,
            'id': id,
            'clientOrderId': order['cid'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': orderType,
            'side': side,
            'average': None,
            'amount': originalAmount,
            'remaining': amount,
            'filled': filled,
            'status': status,
            'fee': None,
            'cost': None,
            'trades': None,
            'hidden': self.safe_value(order, 'hidden'),
        }
        if 'limitPrice' in order:
            resultOrder['price'] = self.safe_float(order, 'limitPrice')
        if 'stopPrice' in order:
            resultOrder['stopPrice'] = self.safe_float(order, 'stopPrice')
        if 'trailingPrice' in order:
            resultOrder['trailingPrice'] = self.safe_float(order, 'trailingPrice')
        if 'futurePrice' in order:
            resultOrder['futurePrice'] = self.safe_float(order, 'futurePrice')
        if 'distance' in order:
            resultOrder['distance'] = self.safe_float(order, 'distance')
        return resultOrder

    def create_deposit_address(self, code, params={}):
        self.load_markets()
        request = {
            'currency': self.currency(code).id,
        }
        response = self.privatePostWalletsCurrencyAddress(self.extend(request, params))
        address = self.safe_value(response, 'address')
        tag = self.safe_value(response, 'tag')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        request = {
            'currency': code,
            'urlParams': {
                'formatted': True,
            },
        }
        response = self.privateGetWalletsCurrencyAddress(self.extend(request, params))
        address = self.safe_value(response, 'address')
        tag = self.safe_value(response, 'tag')
        self.check_address(address)
        return {
            'currency': self.currency(code).id,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        urlParams = {}
        request = {'urlParams': urlParams}
        start = since is not since if None else 0
        urlParams['start'] = start
        urlParams['end'] = self.milliseconds()
        if limit is not None:
            urlParams['limit'] = limit
        response = None
        if code is not None:
            request['currency'] = self.currency(code).id
            response = self.privateGetWalletsCurrencyDeposits(self.extend(request, params))
        else:
            response = self.privateGetDeposits(self.extend(request, params))
        deposits = self.safe_value(response, 'items')
        for i in range(0, len(deposits)):
            deposits[i]['type'] = 'DEPOSIT'
        return self.parse_transactions(deposits, None, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        urlParams = {}
        request = {'urlParams': urlParams}
        if since is not None:
            request['form'] = since
        start = since is not since if None else 0
        urlParams['start'] = start
        urlParams['end'] = self.milliseconds()
        if limit is not None:
            urlParams['limit'] = limit
        response = None
        if code is not None:
            request['currency'] = self.currency(code).id
            response = self.privateGetWalletsCurrencyWithdrawals(self.extend(request, params))
        else:
            response = self.privateGetWithdrawals(self.extend(request, params))
        withdrawals = self.safe_value(response, 'items')
        for i in range(0, len(withdrawals)):
            withdrawals[i]['type'] = 'WITHDRAWAL'
        return self.parse_transactions(withdrawals, None, since, limit)

    def parse_transaction(self, transaction, currency=None):
        timestamp = self.safe_integer(transaction, 'timestamp')
        updated = self.safe_integer(transaction, 'updated')
        currencyId = self.safe_string(transaction, 'currencyCode')
        code = self.safe_currency_code(currencyId, currency)
        type = self.safe_string_lower(transaction, 'type')  # DEPOSIT or WITHDRAWAL
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        feeCost = self.safe_float(transaction, 'fee')
        if feeCost is not None:
            feeCost = abs(feeCost)
        return {
            'info': transaction,
            'id': self.safe_string(transaction, 'id'),
            'txid': self.safe_string(transaction, 'txHash'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': self.safe_string(transaction, 'walletId'),  # todo: self is actually the tag for XRP transfers(the address is missing)
            'tag': None,  # refix it properly for the tag from description
            'type': type,
            'amount': self.safe_float(transaction, 'amount'),
            'currency': code,
            'status': status,
            'updated': updated,
            'fee': {
                'currency': code,
                'cost': feeCost,
                'rate': None,
            },
        }

    def parse_transaction_status(self, status):
        statuses = {
            'PROCESSED': 'pending',
            'CANCELED': 'canceled',
            'COMPLETED': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        destination = address
        if tag is not None:
            destination = address + ':' + tag
        fee = currency.fee
        request = {
            'currency': currency.id,
            'amount': self.sum(amount, fee),
            'fee': fee,
            'currencyCode': currency.id,
            'destination': destination,
        }
        response = self.privatePostWithdrawalsCurrency(self.extend(request, params))
        return {
            'info': response,
            'id': self.safe_string(response, 'id'),
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        apiUrls = self.urls['api']
        urlParams = self.safe_value(query, 'urlParams')
        url = apiUrls[api] + request
        urlParamsStr = self.urlencode(urlParams) if (urlParams is not None) else ''
        if urlParamsStr != '':
            url += '?' + urlParamsStr
        requestBody = self.omit(query, 'urlParams')
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            urlPath = self.options['paths']['private'] + request
            payloadSuffix = ''
            if method != 'GET' and method != 'DELETE':
                body = self.json(requestBody)
                payloadSuffix = body
            payload = '/api' + urlPath + nonce + payloadSuffix
            payload = self.encode(payload)
            secret = self.encode(self.secret)
            signature = self.hmac(payload, secret, hashlib.sha384).upper()
            contentType = 'application/json; charset=UTF-8'
            headers = {
                'Content-Type': contentType,
                'nominex-nonce': nonce,
                'nominex-apikey': self.apiKey,
                'nominex-signature': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if code >= 400:
            if body[0] == '{':
                feedback = self.id + ' ' + body
                if 'code' in response:
                    code = self.safe_string(response, 'code')
                    self.throw_exactly_matched_exception(self.exceptions, code, feedback)
                if 'codes' in response:
                    codes = self.safe_string(response, 'codes')
                    code = self.asString(codes[0])
                    self.throw_exactly_matched_exception(self.exceptions, code, feedback)
                raise ExchangeError(feedback)  # unknown message
            elif body[0] == '[':
                feedback = self.id + ' ' + body
                error = response[0]
                code = self.safe_string(error, 'code')
                self.throw_exactly_matched_exception(self.exceptions, code, feedback)
                raise ExchangeError(feedback)  # unknown message
