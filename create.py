#imports
import datetime, requests
from bs4 import BeautifulSoup
from collections import namedtuple
from harvester import fetch
import random, string

URL = "https://play.cparmies.net/create_account/create_account.php"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', 'x-requested-with': 'ShockwaveFlash/32.0.0.403'
}

def generate_name(n):
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return x

username = generate_name(10)
filename = "accounts.txt"

server_address = ('127.0.0.1', 5000)
token = fetch.token(server_address)

try:
    sess = requests.Session()
    payload = {
        'lang': 'en',
        'affiliate': 0,
        'agree_to_terms': 1,
        'agree_to_rules': 1,
        'action': 'validate_agreement'
    }
    post_login_html = sess.post(URL, data=payload, headers=HEADERS).text
    print("Step 1 result: "+post_login_html)
except Exception as e:
    print(e)
finally:
    try:
        payload = {
            'lang': 'en',
            'username': username,
            'colour': 1,
            'action': 'validate_username'
        }
        post_name_html = sess.post(URL, data=payload, headers=HEADERS).text
        print("Step 2 result: "+post_name_html)
    except Exception as e:
        print(e)
    finally:
        try:
            sid = post_name_html.split("&")
            payload = {
                'lang': 'en', 
                'gtoken': token,
                'email': username + '@gmail.com',
                'password_confirm': '04012001',
                'password': '04012001',
                'action': 'validate_password_email',
                'sid': sid[1][4:]
            }
            post_password_html = sess.post(URL, data=payload, headers=HEADERS).text
            print("Step 3 result: "+post_password_html)
        except Exception as e:
            print(e)
        finally:
            with open("accounts.txt", "a") as myfile:
                myfile.write("username: " + username + " | password: 04012001 \n")
