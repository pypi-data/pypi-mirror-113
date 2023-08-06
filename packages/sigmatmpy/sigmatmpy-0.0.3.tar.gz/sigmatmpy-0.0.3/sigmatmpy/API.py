name = "sigmatmpy"
import requests
import json


class API(object):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.domain = 'http://47.90.247.3:34338/api/'
        self.refresh_token(username,password)
        

    def refresh_token(self,username,password):
        login_url = self.domain + 'Auth'
        token = requests.post(login_url, json = {
            "username": username,
            "password": password
        })
        print(token.json())
        self.token = token.json()['token']
    
    # def get_alert_data(self,alert):

    #     link = f'https://api-pk-data.sigmatm.com.au/api/v1/alert/data?broker_id=2&alert={alert}'
    #     response = requests.get(link , headers={'Authorization': f'Bearer {self.token}'})
    #     return response.json()

    def open_order(self,symbol, cmd, volume, price, slippage, stoploss, takeprofit):
        params = {
                "symbol":symbol,
                "cmd":cmd,
                "volume":volume,
                "price":price,
                "slippage":slippage,
                "stoploss":stoploss,
                "takeprofit":takeprofit
            }
        link = self.domain + 'OrderOpen'
        # print(self.token)
        response = requests.post(link, data = params, headers = {'TOKEN': f'{self.token}'})
        return response.json()

    def close_order(self,ticket, lots, price):
        params = {
                "ticket":ticket,
                "lots":lots,
                "price":price
            }
        link = self.domain + 'OrderClose'
        response = requests.post(link,data = params, headers = {'TOKEN': f'{self.token}'})
        return response.json()


    def trades_user_history(self, login , start_time, end_time):

        link = self.domain + 'TradesUserHistory' + '/' + login + '/' + start_time + '/' + end_time
        response = requests.get(link, headers={'TOKEN': f'{self.token}'})
        return response.json()


    def trades_user_history2(self, login , start_time, end_time):

        link = self.domain + 'TradesUserHistory2' + '/' + login + '/' + start_time + '/' + end_time
        response = requests.get(link, headers={'TOKEN': f'{self.token}'})
        return response.json()

    def opened_trades(self, login ):

        link = self.domain + 'TradesRequest' + '/' + login 
        response = requests.get(link, headers={'TOKEN': f'{self.token}'})
        return response.json()

    def margin(self, login):

        link = self.domain + 'Margin' + '/' + login 
        response = requests.get(link, headers={'TOKEN': f'{self.token}'})
        return response.json()