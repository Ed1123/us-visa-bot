import requests

from creds import chat_id, token


def send_message(text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    parameters = {'chat_id': chat_id, 'text': text}
    return requests.post(url, parameters)


def send_photo(photo_file):
    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    parameters = {'chat_id': chat_id}
    return requests.post(url, parameters, files={'photo': photo_file})


if __name__ == "__main__":
    # Testing
    import json
    import pprint as pp

    print('Sending a test message.')
    response = send_message('Testing')
    response_json = json.loads(response.text)
    print('Results:')
    pp.pprint(response_json)
    assert response_json['ok']

    with open('archive/test.png', 'rb') as f:
        response = json.loads(send_photo(f).text)
    pp.pprint(response)
    assert response['ok']
