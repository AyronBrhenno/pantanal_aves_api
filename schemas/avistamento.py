from pydantic import BaseModel


class AvistamentoSchema(BaseModel):
    """Define como um novo avistamento deve ser representado ao ser
    registrado. Deve estar vinculado a uma espécie já cadastrada,
    identificada pelo nome popular.
    """

    nome_popular: str = "Tuiuiú"
    local: str = "Rio Cuiabá, Barão de Melgaço - MT"
    data_avistamento: str = "15/09/2026"
    observador: str | None = "Ayron"
    quantidade: int | None = 1
    condicoes_climaticas: str | None = "Ensolarado"


class AvistamentoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura para localizar um avistamento
    específico, a partir do seu id.
    """

    id: int = 1


class AvistamentoDelSchema(BaseModel):
    """Define a estrutura retornada após a remoção de um avistamento."""

    mensagem: str
    id: int
