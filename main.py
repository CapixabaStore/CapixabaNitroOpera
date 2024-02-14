import json
import requests
import time
import string
import random

with open('api.json', 'r') as start_file:
    start_data = json.load(start_file)


SCRAPEOPS_API_KEY = start_data.get('api_key', '')

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def get_random_user_agent():
    url = 'http://headers.scrapeops.io/v1/user-agents?api_key=' + SCRAPEOPS_API_KEY
    response = requests.get(url)
    json_response = response.json()
    user_agents = json_response.get('result', [])
    if user_agents:
        return user_agents[random.randint(0, len(user_agents) - 1)]
    else:
        return None

def start_process():
    url = 'https://api.discord.gx.games/v1/direct-fulfillment'
    headers = {
        'authority': 'api.discord.gx.games',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.opera.com',
        'referer': 'https://www.opera.com/',
        'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
    }

    data = {
        'partnerUserId': generate_random_string(64)
    }

    session = requests.Session()

    try:
        last_user_agent_change_time = time.time()
        request_count = 0
        is_429_printed = False

        while True:

            current_time = time.time()
            if current_time - last_user_agent_change_time >= 12:
                print("\033[93m[Alerta]\033[0m Trocando o Ip. Aguarde um Momento...")
                random_user_agent = get_random_user_agent()
                if random_user_agent:
                    headers['user-agent'] = random_user_agent
                    print(f"\033[92m[INFO]\033[0m Usuario Ip: {random_user_agent}")
                    last_user_agent_change_time = current_time

            response = session.post(url, headers=headers, json=data)
            request_count += 1

            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    try:
                        with open('capixaba.txt', 'a') as file:
                            file.write(f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n")
                            print(f"\033[92m[INFO]\033[0m https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n")
                    except Exception as error:
                        print(f"\033[91m[ERROR]\033[0m Erro no Processamento do Arquivo: {str(error)}")
            elif response.status_code == 429:
                if not is_429_printed:
                    print("\033[93m[Alerta]\033[0m 429 ERRO RECEBIDO. Aguarde...")
                    is_429_printed = True
                    while response.status_code == 429:
                        time.sleep(60)  # Wait for 60 seconds before checking again
                        response = session.post(url, headers=headers, json=data)
                    is_429_printed = False
                else:
                    time.sleep(0)
            else:
                print(f"Projeto com erro, status code: {response.status_code}.")
                print(f"Error message: {response.text}")

            time.sleep(0.5)

    except Exception as error:
        print(f"\033[91m[ERROR]\033[0m erro ocorrido: {str(error)}")

    finally:
        session.close()

if __name__ == "__main__":
    while True:
        print("1. Começar Farm")
        print("2. Sair")
        choice = input("Digite o numero: ")

        if choice == "1":
            start_process()
        elif choice == "2":
            print("Saindo do Programa.")
            break
        else:
            print("Opção invalida. escolha 1 ou 2.")
