import http.client
import json

def send(id, token, text):
    connection = http.client.HTTPSConnection("api.telegram.org")
    headers = {'Content-type': 'application/json'}
    data = {'chat_id': id, 'text': text}
    path = "/bot" +token + "/sendMessage"
    connection.request('POST', path, json.dumps(data), headers)
    response = connection.getresponse()
    #print(response.read().decode())
