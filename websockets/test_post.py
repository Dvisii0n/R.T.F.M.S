import urllib.request
import json

data = json.dumps({'message': 'test event'}).encode('utf-8')
req = urllib.request.Request('http://localhost:8081/send_event', data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        print('Response:', response.read().decode())
except Exception as e:
    print('Error:', e)