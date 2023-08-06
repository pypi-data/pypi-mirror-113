name = "sigmatmpy"
import requests
import json
import asyncio
import websocket 


class API(object):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.domain = 'http://47.90.247.3:34338/api/'
        self.domain_ws = 'ws://47.90.247.3:34338/api/PriceStream/'
        self.refresh_token(username,password)
        self.price = None
        self.bars = {}
        

    def refresh_token(self,username,password):
        login_url = self.domain + 'Auth'
        token = requests.post(login_url, json = {
            "username": username,
            "password": password
        })
        self.token = token.json()['token']

    def open_order(self,symbol, cmd, volume, price, slippage, stoploss, takeprofit, comment):
        params = {"symbol":symbol,"cmd":cmd,"volume":volume,"price":price,"slippage":slippage,"stoploss":stoploss,"takeprofit":takeprofit,"comment":comment}

        link = self.domain + 'OrderOpen'
        
        # print(self.token)
        response = requests.post(link, data = json.dumps(params), headers = {'TOKEN': f'{self.token}','Content-Type' : 'application/json; charset=utf-8'})
        return response.json()

    def close_order(self,ticket, lots, price):
        params = {"ticket":ticket,"lots":lots,"price":price}
        link = self.domain + 'OrderClose'
        response = requests.post(link,data = json.dumps(params), headers = {'TOKEN': f'{self.token}','Content-Type' : 'application/json; charset=utf-8'})
        return response.json()

    def trades_history_by_datetime(self, start_time, end_time):

        link = self.domain + 'TradesUserHistory' + '/' + start_time + '/' + end_time
        response = requests.get(link, headers = {'TOKEN': f'{self.token}'})
        return response.json()

    def trades_history_by_unixtime(self, start_time_ctm, end_time_ctm):

        link = self.domain + 'TradesUserHistory2' + '/' + str(start_time_ctm) + '/' + str(end_time_ctm)
        response = requests.get(link, headers = {'TOKEN': f'{self.token}'})
        return response.json()

    def opened_trades(self):

        link = self.domain + 'TradesRequest'
        response = requests.get(link, headers = {'TOKEN': f'{self.token}'})
        return response.json()

    def account_info(self):

        link = self.domain + 'Margin' + '/'
        response = requests.get(link, headers = {'TOKEN': f'{self.token}'})
        return response.json()

    def symbol_info(self, symbol):

        link = self.domain + 'SymbolsGet' + '/' + symbol
        response = requests.get(link, headers = {'TOKEN': f'{self.token}'})
        return response.json()
    
    def initialize_price_stream(self, symbol, timeframe):
        self.price = websocket.create_connection(self.domain_ws + symbol,header={'TOKEN': self.token})
        self.bars[timeframe] = self.bar_chart(symbol, timeframe)[-1]['Ctm']

    def current_price(self):
        return json.loads(self.price.recv())
    
    def server_time(self):
        link = self.domain + 'ServerTime'
        response = requests.get(link, headers = {'TOKEN': f'{self.token}'})
        return response.json()

    def bar_chart(self, symbol, timeframe):
        link = self.domain + 'ChartRequest/' + symbol + '/' + str(timeframe)
        response = requests.get(link, headers = {'TOKEN': f'{self.token}'})
        digit = self.symbol_info(symbol)['Digits']
        result = response.json()
        for key in range(len(result)):
            result[key]['Open'] =round(result[key]['Open'] * (10**-digit), digit)
            result[key]['Close'] = round((result[key]['Close'] * (10**-digit)) + result[key]['Open'], digit)
            result[key]['High'] = round((result[key]['High'] * (10**-digit)) + result[key]['Open'], digit)
            result[key]['Low'] = round((result[key]['Low'] * (10**-digit)) + result[key]['Open'], digit)
        return result

    def check_new_bar(self,symbol,timeframe):
        if self.bar_chart(symbol,timeframe)[-1]['Ctm'] == self.bars[timeframe]:
            return False
        else:
            self.bars[timeframe] = self.bar_chart(symbol,timeframe)[-1]['Ctm'] 
            return True