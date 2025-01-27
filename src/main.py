import requests
import json
import os 
from dotenv import load_dotenv
from functools import wraps


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_TOKEN = os.getenv("API_TOKEN")


def manage_request(function):
    """Decorator to handle requests and process their response."""
    @wraps(function)
    def wrapper(self, request_function):
        try:
            response = function(self, request_function)

            #check error status code (400 a 599) and throws an exception.
            response.raise_for_status()
            response = response.json()
            print("Requisição bem-sucedida.")
            return response

        except requests.exceptions.RequestException as err:
            print(f"Erro durante requisição:\n{err}")
            return None

        except json.JSONDecodeError as err:
            print(f"Erro ao decodificar JSON.\n{err}")
            return None

    return wrapper


class Trello():
    """Class for manager API Trello requests."""

    def __init__(self, api_key: str, api_token: str):
        """
        Initialize the class with API Key and Token.

        :param api_key: Trello key API\n
        :param api_token: Trello API token
        """
        self.api_key = api_key
        self.api_token = api_token
        self.BASE_URL = "https://api.trello.com/"
        self.KEY_TOKEN_URL = f"key={API_KEY}&token={API_TOKEN}"
        self.query = {
            "key": f"{API_KEY}",
            "token": f"{API_TOKEN}"
        } 

    @staticmethod
    def save_json(data: dict, path: str):
        """
        Save json response of API in json file.

        :param data: dict that will be saved.
        :param path: path where you'll be saved.
        """
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except IOError as err:
            print(f"Error saving file:\n{err}")


    @manage_request
    def _make_request(self, request_function):
        """
        Makes an HTTP request using the provided function.

        :param requets_function: Requests function like requests.get(url).
        :return: JSON from the requests.
        """
        return request_function()


    def get_all_my_boards(self) -> (dict | None):
        """
        Request to get all my boards.

        :return: dict -  request json response.
        """
        return self._make_request(lambda: requests.get(url=f"{self.BASE_URL}1/members/me/boards?fields=name&{self.KEY_TOKEN_URL}"))


    def get_board(self, id_board: str) -> (dict | None):
        """
        Get more details board.

        :param id_board: ID of the board you want more details.

        :return: dict - request json response.
        """
        return self._make_request(lambda: requests.get(url=f"{self.BASE_URL}1/boards/{id_board}?{self.KEY_TOKEN_URL}"))
            

    def get_card():
        ...


def main():
    my_trello = Trello(api_token=API_TOKEN, api_key=API_KEY)
    all_my_boards = my_trello.get_all_my_boards()

    if all_my_boards:
        my_trello.save_json(data=all_my_boards, path="../json/get_all_my_boards.json")

        for item in all_my_boards:
            board = my_trello.get_board(item["id"])
            if board:
                my_trello.save_json(data=board, path=f"../json/board_{item['id']}.json")
            else:
                print("Requisição get_board falhou.")

    else:
        print("Requisição get_all_my_boards falhou.")


if __name__ == "__main__":
    main()
