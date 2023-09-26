import requests
from capmonster_python import CapmonsterException, HCaptchaTask


class IrpfSituationService:
    """Service to get the IRPF situation using web scraping"""

    page_link = "https://www.restituicao.receita.fazenda.gov.br"
    website_key = "1e7b8462-5e38-4418-9998-74210d909134"

    async def __get_hcaptcha_token(self):
        for _ in range(5):
            try:
                capmonster = HCaptchaTask("26d6e1876ace493aa2bb1a73c30012f9")
                task_id = capmonster.create_task(self.page_link, self.website_key)
                result = capmonster.join_task_result(task_id)
                return result.get("gRecaptchaResponse")
            except CapmonsterException:
                print("Retrying...")

        print("Failed")
        raise ValueError

    async def get_situation(self, data: dict) -> str:
        """Get the IRPF situation using web scraping"""
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
            "h-captcha-response": await self.__get_hcaptcha_token(),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "token": "",
            "token_fcm": "",
            "X-Firebase-AppCheck": "",
            "token_esuite": "",
            "Connection": "keep-alive",
        }
        url = f"{self.page_link}/servicos-rfb-apprfb-restituicao/apprfb-restituicao/consulta-restituicao"
        resp = requests.get(
            f"{url}/{data['cpf']}/{data['year']}/{data['birth_date']}",
            proxies={
                "http": "http://968dd11a07064121908e1d9078f0dfaa:@proxy.crawlera.com:8011/",
                "https": "http://968dd11a07064121908e1d9078f0dfaa:@proxy.crawlera.com:8011/",
            },
            headers=headers,
            timeout=30,
            verify=False,
        )

        print(resp.status_code, resp.text)

        restituicao = resp.json()

        if (restituicao["restituicao"] or {}).get("situacaoRestituicao"):
            return restituicao["restituicao"]["situacaoRestituicao"]

        return restituicao["situacao"]
