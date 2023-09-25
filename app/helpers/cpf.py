async def validate_and_clean_cpf(cpf: str):
    """Validate and clean cpf"""
    if not cpf:
        raise ValueError("CPF não informado.")

    cpf = cpf.replace(".", "").replace("-", "")
    if not cpf.isnumeric():
        raise ValueError("CPF inválido.")
    
    if len(cpf) != 11:
        raise ValueError("CPF inválido.")

    return cpf