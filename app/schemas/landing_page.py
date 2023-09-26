from pydantic import BaseModel


class PriorityData(BaseModel):
    """Data priority to save in db"""

    cpf: str
    birth_date: str
    address: dict = {
        "street": "Rua dos Bobos",
        "house_number": "0, Apto 0",
        "district": "Vila do Chaves",
        "city": "São Paulo",
        "state": "SP",
        "cep": "00000-000",
    }
    email: str
    phone: str
