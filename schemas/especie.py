from pydantic import BaseModel

from model.especie import Especie


class EspecieSchema(BaseModel):
    """Define como uma nova espécie a ser inserida deve ser representada."""

    nome_popular: str = "Tuiuiú"
    nome_cientifico: str | None = "Jabiru mycteria"
    familia: str | None = "Ciconiidae"
    status_conservacao: str | None = "Pouco preocupante"


class EspecieBuscaSchema(BaseModel):
    """Define como deve ser a estrutura de busca, feita apenas com base
    no nome popular da espécie.
    """

    nome_popular: str = "Tuiuiú"


class ListagemEspeciesSchema(BaseModel):
    """Define como a listagem de espécies será retornada."""

    especies: list[EspecieSchema]


class EspecieViewSchema(BaseModel):
    """Define como uma espécie será retornada: dados da espécie + a lista
    de avistamentos registrados para ela.
    """

    id: int = 1
    nome_popular: str = "Tuiuiú"
    nome_cientifico: str | None = "Jabiru mycteria"
    familia: str | None = "Ciconiidae"
    status_conservacao: str | None = "Pouco preocupante"
    total_avistamentos: int = 1


class EspecieDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma
    requisição de remoção de espécie.
    """

    mensagem: str
    nome_popular: str


def apresenta_especies(especies: list[Especie]):
    """Retorna uma representação resumida das espécies, sem a lista
    completa de avistamentos (usado na listagem geral).
    """
    result = []
    for especie in especies:
        result.append(
            {
                "id": especie.id,
                "nome_popular": especie.nome_popular,
                "nome_cientifico": especie.nome_cientifico,
                "familia": especie.familia,
                "status_conservacao": especie.status_conservacao,
                "total_avistamentos": len(especie.avistamentos),
            }
        )
    return {"especies": result}


def apresenta_especie(especie: Especie):
    """Retorna uma representação completa da espécie, incluindo a lista
    de avistamentos vinculados a ela.
    """
    return {
        "id": especie.id,
        "nome_popular": especie.nome_popular,
        "nome_cientifico": especie.nome_cientifico,
        "familia": especie.familia,
        "status_conservacao": especie.status_conservacao,
        "total_avistamentos": len(especie.avistamentos),
        "avistamentos": [
            {
                "id": a.id,
                "local": a.local,
                "observador": a.observador,
                "quantidade": a.quantidade,
                "condicoes_climaticas": a.condicoes_climaticas,
                "data_avistamento": a.data_avistamento.strftime("%d/%m/%Y"),
            }
            for a in especie.avistamentos
        ],
    }
