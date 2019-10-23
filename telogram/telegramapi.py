import http.client
import json

def send(token, id, text):
    connection = http.client.HTTPSConnection("api.telegram.org")
    headers = {'Content-type': 'application/json'}
    data = {'chat_id': id, 'text': text}
    connection.request('POST', "/bot" +token + "/sendmessage", json.dumps(data), headers)

