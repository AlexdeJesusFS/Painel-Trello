import main
import os 
from dotenv import load_dotenv
import requests
import json


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = "https://api.trello.com/"
KEY_TOKEN_URL = f"key={API_KEY}&token={API_TOKEN}"

trello = main.Trello(api_key=API_KEY, api_token=API_TOKEN)


def _make_request(fun):
    try:
        response = fun

        #check error status code (400 a 599) and throws an exception.
        response.raise_for_status()
        response = response.json()
        print("Requisição get_all_my_boards bem-sucedida.")
        return response

    except requests.exceptions.RequestException as err:
        print(f"Erro durante requisição get_all_my_boards:\n{err}")
        return None

    except json.JSONDecodeError as err:
        print(f"Erro ao decodificar JSON.\n{err}")
        return None


_make_request(requests.get(url=f"{BASE_URL}1/members/me/boards?fields=name&{KEY_TOKEN_URL}"))

