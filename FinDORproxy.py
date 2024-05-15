from mitmproxy import http
import re
import os
import sys
import argparse
import pyfiglet
from colorama import Fore

class IDORDetector:
    def __init__(self):
        self.patternGET1 = re.compile(r'(?:[?&]|/)([a-zA-Z]+)?[a-zA-Z_]*[id|ID|name|NAME|nama|NAMA|user|USER]=(\w+)|/(\d+)(?:\.\w+)?/?$', re.IGNORECASE)
        self.patternGET2 = re.compile(r'/(\d+)', re.IGNORECASE)
        self.patternGET3 = re.compile(r'[?&/](?:[a-zA-Z_]*[a-zA-Z])(?:=|/)([a-zA-Z0-9_]+)', re.IGNORECASE)

        self.paternPOST1 = re.compile(r'"[a-zA-Z_]*[Id]":"([^"]+)"', re.IGNORECASE)
        self.paternPOST2 = re.compile(r'[a-zA-Z_]*[Id]=([^"&]+)', re.IGNORECASE)
        self.paternPOST3 = re.compile(r'[a-zA-Z_]*[Id]%5D=([^"&]+)', re.IGNORECASE)
        self.idor_count = 0
        if sys.platform.startswith('win'):
            self.user_dir = os.path.join(os.getenv('USERPROFILE'), 'Documents', 'Potential IDOR')
        else:
            self.user_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'Potential IDOR')
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

    def request(self, flow: http.HTTPFlow):
        if flow.request.method == "GET" or flow.request.method == "POST":
            if flow.request.method == "GET" and self.patternGET1.search(flow.request.url):
                self.idor_count += 1
                self.save_get_request_to_file(flow)
            elif flow.request.method == "GET" and self.patternGET2.search(flow.request.url):
                self.idor_count += 1
                self.save_get_request_to_file(flow)
            elif flow.request.method == "GET" and self.patternGET3.search(flow.request.url):
                self.idor_count += 1
                self.save_get_request_to_file(flow)
            elif flow.request.method == "POST" and self.paternPOST1.search(flow.request.text):
                self.idor_count += 1
                self.save_post_request_to_file(flow)
            elif flow.request.method == "POST" and self.paternPOST2.search(flow.request.text):
                self.idor_count += 1
                self.save_post_request_to_file(flow)
            elif flow.request.method == "POST" and self.paternPOST3.search(flow.request.text):
                self.idor_count += 1
                self.save_post_request_to_file(flow)

    def save_get_request_to_file(self, flow: http.HTTPFlow):
        authorization_token = flow.request.headers.get('Authorization')
        cookie = flow.request.headers.get('Cookie')
        filename = os.path.join(self.user_dir, f'potential_idor_request{self.idor_count}.txt')
        with open(filename, "w") as f:
            f.write(f"URL: {flow.request.pretty_url}\n")
            if authorization_token:
                f.write(f"Authorization Token: {authorization_token}\n\n")
            else:
                f.write("No Authorization Token found.\n\n")
            if cookie:
                f.write(f"Cookie: {cookie}\n\n")
            else:
                f.write("No Cookie found.\n\n")

    def save_post_request_to_file(self, flow: http.HTTPFlow):
        filename = os.path.join(self.user_dir, f'potential_idor_request{self.idor_count}.txt')
        with open(filename, "w") as f:
            f.write(f"{flow.request.method} {flow.request.path} HTTP/1.1\n")
            if(flow.request.port is not None):
                f.write(f"Host: {flow.request.host}" + f":{flow.request.port}\n")
            elif(flow.request.port is None):
                f.write(f"Host: {flow.request.host}\n")
            f.write(f"User-Agent: {flow.request.headers.get('User-Agent')}\n")
            f.write(f"Cookie: {flow.request.headers.get('Cookie')}\n")
            f.write(f"Content-Type: {flow.request.headers.get('Content-Type')}\n")
            f.write(f"Content-Length: {flow.request.headers.get('Content-Length')}\n")
            f.write(f"Origin: {flow.request.headers.get('Origin')}\n")
            f.write(f"Referer: {flow.request.headers.get('Referer')}\n")
            f.write(f"Sec-Fetch-Dest: {flow.request.headers.get('Sec-Fetch-Dest')}\n")
            f.write(f"Sec-Fetch-Mode: {flow.request.headers.get('Sec-Fetch-Mode')}\n")
            f.write(f"Sec-Fetch-Site: {flow.request.headers.get('Sec-Fetch-Site')}\n")
            f.write(f"Te: {flow.request.headers.get('Te')}\n")
            f.write(f"Connection: {flow.request.headers.get('Connection')}\n\n")
            f.write(flow.request.text)

addons = [
    IDORDetector()
]

def printLogo():
    logo = pyfiglet.figlet_format("FinDOR Proxy", font="slant")
    print( Fore.CYAN + logo + Fore.RESET)
    print(Fore.CYAN + "\t\t\t"+ "Version 1.0" + Fore.RESET)
    print("")

def main():

    printLogo()

    parser = argparse.ArgumentParser(description='FinDOR Proxy Helpguide: ')
    parser.add_argument('-p', '--port', dest='port_service', help='Input Port Target to Start Proxy Service')

    args = parser.parse_args()

    if(args.port_service):
        start(args.port_service)
    else:
        start(port_service=8081)

def start(port_service):
    print("[" + Fore.BLUE + "*" + Fore.RESET + "]" + " Proxy Listener" + Fore.LIGHTGREEN_EX + " Started" + Fore.RESET + " on Port" + Fore.LIGHTYELLOW_EX + f" {port_service}" + Fore.RESET)
    from mitmproxy.tools.main import mitmproxy
    mitmproxy(['-p', f'{port_service}', '-s', __file__])

if __name__ == "__main__":
    main()