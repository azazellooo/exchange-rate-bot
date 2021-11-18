import requests


class ApiSource:
    def __init__(self, base_url):
        self.base_url = base_url

    def make_request(self, url):
        return requests.get(f'{self.base_url}/{url}').json()


class ExchangeRateApiSource(ApiSource):

    def get_latest_info(self):
        data = self.make_request('latest?base=USD')
        latest_info = ''
        if data.get('success'):
            for rate, amount in data.get('rates').items():
                latest_info += f'{rate}: {amount} \n'
        return latest_info

    def convert_currency(self, curr_from, curr_to, amount=1):
        data = self.make_request(f'convert?from={curr_from}&to={curr_to}&amount={amount}')
        response = ''
        if data.get('success'):
            result = data.get('result')
            response += f'{amount} {curr_from} = {result} {curr_to}'
        return response
