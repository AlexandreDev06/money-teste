import requests

from app.configs.settings import settings


class Zapsign:
    """Class to handle external requests"""

    async def send_contract_zapsign(self, data: dict):
        """Send the contract to the zapsign API

        Args:
            data (dict): The data that contain data about the property and the client
        """
        is_prod = settings.environment == "production"

        if not is_prod:
            data["email"] = "lhm.ambiental@gmail.com"

        url = "https://api.zapsign.com.br/api/v1/models/create-doc/"
        querystring = {"api_token": settings.zap_sign_token}
        payload = {
            "sandbox": not is_prod,
            "template_id": "bce3495a-c6d4-4258-8935-94344164b591",
            "signer_name": data["name"],
            "external_id": f"recdinmoney-{data['client_id']}",
            "send_automatic_email": True,
            "data": [
                {"de": "{{NOME COMPLETO}}", "para": data["name"]},
                {"de": "{{NÚMERO DO CPF}}", "para": data["cpf"]},
                {"de": "{{ENDEREÇO COMPLETO}}", "para": data["address"]},
                {"de": "{{DATA DE NASCIMENTO}}", "para": data["birth_date"]},
                {"de": "{{EMAIL CLIENTE}}", "para": data["email"]},
                {"de": "{{ANO}}", "para": data["year"]},
            ],
        }
        resp = requests.post(url, json=payload, params=querystring, timeout=60)

        if resp.status_code == 200:
            print("Contract sent to zapsign")
            # return code to url zapsign
            # return resp.json()["signers"][1]["sign_url"].split("/")[-1]

        else:
            print("Error sending contract to zapsign")
            print(resp.status_code, resp.json())
