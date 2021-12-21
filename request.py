import requests
import time
import urllib3
#urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)
x=0
while True:

    data=requests.post('https://192.168.1.89:8000/', verify= 'Cert.pem',json = {"id" : x })
    x=x+1
    time.sleep(1)
    if x > 1000:
        x=0
#print(data.text)

