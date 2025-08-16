import requests
import json

url = "http://httpbin.org/get"

r = requests.get(url)

print("url: {} \n".format(r.url))
print("Status: {} \n".format(r.status_code))
print("Header: {} \n".format(r.headers))
print("Text Output: {} \n".format(r.text))
#print("Jsong Output: {} \n".format(r.json()))

if r.status_code == 200:
    print("Success!")
elif r.status_code == 404:
    print("Not Found")
elif r.status_code == 500:
    print("Internal Server Error")
else:
    print(f"Other Error: {r.status_code}")
