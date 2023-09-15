from re import search
from time import sleep

import requests

from app.configs.settings import settings


class Volpe:
    def __init__(self):
        self.api_key = settings.volpe_api_key
        self.url = settings.volpe_url

    def search_cpf_data(self, cpf: str, force: bool = False):
        """Get volpe data from api"""
        cpf = cpf.replace(".", "").replace("-", "")
        headers = {"Content-Type": "application/json"}
        params = {"serasa": False, "force": force, "api_key": self.api_key}
        response = requests.get(
            f"{self.url}data/{cpf}/task", headers=headers, params=params, timeout=20
        )
        if response.status_code != 200:
            print(f"Error ao buscar dados no hub Volpe do CPF: {cpf}")
            print(response.status_code)
            return None

        if response.json().get("data"):
            return response.json()["data"]

        task_id = response.json()["task_id"]
        for _ in range(9):
            sleep(10)
            response = requests.get(
                f"{self.url}data/{task_id}/check",
                headers=headers,
                params={"api_key": self.api_key},
            )

            if response.json().get("data"):
                print("Successfully requested data from volpe HUB")
                return response.json()["data"]

            if response.json()["detail"]["status"] == "error":
                print(response.json()["error"])
                return None

    def search_data_volpe(
        self, key: str, data: dict, is_array: bool = False, search_number: int = 0
    ):
        """Search data in the volpe json"""
        full_list = []

        # Search data in the different API keywords in the JSON data
        for key_api in ["procob", "assertiva", "direct_data", "serasa"]:
            print(data)
            full_list += data[key_api][key]

        # Return array if is_array is true
        if is_array:
            rgx = r"@ig|@terra|@uol|@bol|@procob"
            return set([item for item in full_list if not search(rgx, item)]) or []

        # Return the value
        if full_list != []:
            return full_list[search_number]

        # If data is null
        print("Error searching " + key + " in the volpe json")
        return ""
