import requests, base64

response = requests.post(
    'http://127.0.0.1:5000/',
    {'data':base64.b64encode(b'unchi')})

print(response.text)
