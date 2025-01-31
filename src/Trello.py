import requests
import json
import os 
from dotenv import load_dotenv
from functools import wraps


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_TOKEN = os.getenv("API_TOKEN")

# Google Docstring Style


def manage_request(function):
    """
    Decorator to handle requests and process their response.
    
    This decorator wraps a function that performs an HTTP request,
    halding potential errors and proper JSON response.

    Args:
        function (Callable): the function that executes the HTTP request.

    Returns:
        Callable: A wrapped function that processes the request.

    Raises:
        request.exceptions.RequestException: If the request encounters an error.
        json.JSONDecodeError: If the response cannot be parsed as JSON.
    """
    @wraps(function)
    def wrapper(self, request_function):
        try:
            response = function(self, request_function)

            #check error status code (400 a 599) and throws an exception.
            response.raise_for_status()
            response = response.json()
            print("Request successful.")
            return response

        except requests.exceptions.RequestException as err:
            print(f"Error during request:\n{err}")
            return None

        except json.JSONDecodeError as err:
            print(f"Error decoding JSON.\n{err}")
            return None

    return wrapper


class Trello():
    """
    A class to manage API requests for Trello.

    This class provides methods to interact with the Trello API, allowing users to 
    perform operations such as retrieving boards, creating cards, and managing lists.

    Attributes:
        api_key (str): The API key for authenticating requests.
        api_token (str): The API token for authentication.
        BASE_URL (str): The base URL for Trello API requests.
        KEY_TOKEN_URL (str): The formatted API key and token query string.
        query (dict): A dictionary containing authentication parameters for requests.
        headers (dict): A dictionary containing the headers for API requests.
    """

    def __init__(self, api_key: str, api_token: str):
        """
        Initializes the Trello API client with the provided API key and token.

        Args:
            api_key (str): The API key for authentication.
            api_token (str): The API token for authentication.
        """
        self.api_key = api_key
        self.api_token = api_token
        self.BASE_URL = "https://api.trello.com/"
        self.KEY_TOKEN_URL = f"key={API_KEY}&token={API_TOKEN}"
        self.query = {
            "key": f"{API_KEY}",
            "token": f"{API_TOKEN}"
        }
        self.headers = {
            "Accept": "application/json"
        }

    @staticmethod
    def save_json(data: dict, path: str):
        """
        Saves a dictionary as a JSON file.

        Writes a given dictionary to a JSON file at the specified path.
        It ensures the file is encoded in UTF-8 and formatted for readability.

        Args:
            data (dict): The dictionary to be saved as a JSON file.
            path (str): The file path where the JSON will be stored.

        Raises:
            IOError: If an error occurs while writing to the file.
        """
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except IOError as err:
            print(f"Error saving file:\n{err}")

    
    @manage_request
    def _make_request(self, request_function) -> dict | None:
        """
        Executes an HTTP request using the provided function.

        This method takes a fully constructed request function (e.g., `requests.get(url)`) 
        and executes it. The request function must be a callable that, when invoked, 
        returns a `requests.Response` object.

        Args:
            request_function (Callable[[], requests.Response]): 
                A function that performs an HTTP request, such as `requests.get(url)` 
                or `requests.put(url, data=...)`.

        Returns:
            dict | None: The JSON response from the request if successful, otherwise `None`.
        """
        return request_function()


    def get_all_my_boards(self) -> dict | None:
        """
        Retrieves all boards associated with the authenticated user.

        Sends a GET request to the Trello API to fetch all boards 
        belonging to the authenticated user. The response includes the board names and ID.

        Returns:
            dict | None: A dictionary containing the JSON response with the boards,
            Dict response if the request is successful. Returns `None` if the request fails.
        """
        return self._make_request(lambda: requests.get(
            url=f"{self.BASE_URL}1/members/me/boards?fields=name", 
            params=self.query, 
            headers=self.headers))


    def get_board_by_id(self, id_board: str) -> dict | None:
        """
        Get more details board.

        Get more information and details about the board informed by your ID.

        Args:
            id_board (str): ID of the board you want more details.

        Returns: 
            dict | None: A dictionary containing the JSON response,
            Dict response if the request is successful. Returns `None` if the request fails.
        """
        return self._make_request(lambda: requests.get(
            url=f"{self.BASE_URL}1/boards/{id_board}", 
            params=self.query, 
            headers=self.headers))


    def get_cards_on_board(self, id_board: str) -> dict | None:
        """
        Get all of the open cards on a board.

        Sends a GET request to the Trello API to fetch all the open cards 
        associated with the provided board ID.

        Args:
            id_board (str): ID of the board.

        Returns:
            dict | None: A dictionary containing the JSON response,
            Dict response if the request is successful. Returns `None` if the request fails.
        """
        return self._make_request(lambda: requests.get(
            url=f"{self.BASE_URL}1/boards/{id_board}/cards",
            params=self.query,
            headers=self.headers
        ))

    def create_webhook(self, id_model: str, description: str, callback_url: str):
        ...



def main():
    my_trello = Trello(api_token=API_TOKEN, api_key=API_KEY)
    all_my_boards = my_trello.get_all_my_boards()

    if all_my_boards:
        my_trello.save_json(data=all_my_boards, path="../json/get_all_my_boards.json")

        for item in all_my_boards:
            board = my_trello.get_board(item["id"])
            cards = my_trello.get_cards_on_board(item["id"])

            if board:
                my_trello.save_json(data=board, path=f"../json/board_{item['id']}.json")
            else:
                print("get_board request failed.")

            if cards:
                my_trello.save_json(data=cards, path=f"../json/cards_{item['id']}.json")
            else:
                print("get_cards_on_board request failed.")

    else:
        print("get_all_my_boards request failed.")


if __name__ == "__main__":
    main()
