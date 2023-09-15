import requests
from capmonster_python import HCaptchaTask


class IrpfSituationService:
    """Service to get the IRPF situation using web scraping"""

    page_link = "https://www.restituicao.receita.fazenda.gov.br/servicos-rfb-apprfb-restituicao/apprfb-restituicao/consulta-restituicao"
    website_key = "1e7b8462-5e38-4418-9998-74210d909134"

    async def get_situation(self, data: dict) -> dict:
        """Get the IRPF situation using web scraping"""
        capmonster = HCaptchaTask("26d6e1876ace493aa2bb1a73c30012f9")
        task_id = capmonster.create_task(self.page_link, self.website_key)
        result = capmonster.join_task_result(task_id)
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.restituicao.receita.fazenda.gov.br/",
            "versao_app": "1.0",
            "aplicativo": "RESTITUICAO",
            "servico": "consultar_restituicao",
            "so": "WE",
            "origem": "web",
            "h-captcha-response": result.get("gRecaptchaResponse"),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "token": "",
            "token_fcm": "",
            "X-Firebase-AppCheck": "",
            "token_esuite": "",
            "Connection": "keep-alive",
        }

        resp = requests.get(
            f"{self.page_link}/{data['cpf']}/{data['exercie']}/{data['data']}",
            proxies={
                "http": "http://968dd11a07064121908e1d9078f0dfaa:@proxy.crawlera.com:8011/"
            },
            headers=headers,
            timeout=30,
            verify=False,
        )
        return resp.json()
