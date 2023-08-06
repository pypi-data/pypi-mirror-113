import requests
import threading


class NotBot():

    __BASE_URL = 'https://api.telegram.org/bot{token}/{endpoint}'

    def __init__(self, token):
        self.__update_url = self.__BASE_URL.format(token=token, endpoint='getUpdates')
        self.__send_url = self.__BASE_URL.format(token=token, endpoint='sendMessage')

    def notify(self, text):
        response = requests.get(self.__update_url)
        response.raise_for_status()

        chat_ids = set(msg['message']['from']['id'] for msg in response.json()['result'])
        for chat_id in chat_ids:
            params = {'chat_id': chat_id, 'text': text}
            requests.get(self.__send_url, params=params)

    def notify_async(self, text):
        notify_thread = threading.Thread(target=self.notify, args=(text,))
        notify_thread.start()
