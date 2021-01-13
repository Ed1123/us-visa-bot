import requests
from creds import token, chat_id


def send_message(text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    parameters = {
        'chat_id': chat_id,
        'text': text
    }
    return requests.post(url, parameters)


def send_photo(photo_file):
    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    parameters = {
        'chat_id': chat_id
    }
    return requests.post(url, parameters, files={'photo': photo_file})


if __name__ == "__main__":
    # Testing
    import json
    import pprint as pp

    # print('Sending a test message.')
    # response = send_message('Testing')
    # response_json = json.loads(response.text)
    # assert response_json['ok']
    # print('Results:')
    # pp.pprint(response_json)

    with open('archive/test.png', 'rb') as f:
        response = json.loads(send_photo(f).text)
    assert response['ok']
    pp.pprint(response)