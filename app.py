from datetime import datetime

from flask import redirect
from flask_cors import CORS
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag
from flask_openapi3.openapi import OpenAPI
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from logger import logger
from model import Avistamento, Especie, Session
from schemas import *

info = Info(
    title="API Diário de Aves do Pantanal",
    version="1.0.0",
    description="API para catalogar espécies de aves e registrar avistamentos "
    "de campo no Pantanal mato-grossense.",
)
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags utilizadas para organizar a documentação
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
especie_tag = Tag(
    name="Espécie",
    description="Cadastro, busca, listagem e remoção de espécies de aves",
)
avistamento_tag = Tag(
    name="Avistamento",
    description="Registro e remoção de avistamentos de campo de uma espécie",
)
estatistica_tag = Tag(
    name="Estatísticas", description="Indicadores gerais do diário de campo"
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


def _parse_data(texto_data: str) -> datetime:
    """Converte uma data no formato DD/MM/AAAA em um objeto datetime.
    Levanta ValueError caso o texto não esteja nesse formato.
    """
    return datetime.strptime(texto_data.strip(), "%d/%m/%Y")


# Espécie


@app.post(
    "/especie",
    tags=[especie_tag],
    responses={"200": EspecieViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_especie(form: EspecieSchema):
    """Cadastra uma nova espécie de ave no diário de campo.

    Retorna a representação da espécie cadastrada.
    """
    especie = Especie(
        nome_popular=form.nome_popular,
        nome_cientifico=form.nome_cientifico or "",
        familia=form.familia or "",
        status_conservacao=form.status_conservacao or "Não avaliado",
    )
    logger.debug(f"Cadastrando espécie: '{especie.nome_popular}'")
    try:
        session = Session()
        session.add(especie)
        session.commit()
        logger.debug(f"Espécie cadastrada: '{especie.nome_popular}'")
        return apresenta_especie(especie), 200

    except IntegrityError:
        error_msg = "Já existe uma espécie cadastrada com esse nome popular :/"
        logger.warning(f"Erro ao cadastrar '{especie.nome_popular}', {error_msg}")
        return {"mensagem": error_msg}, 409

    except ValueError:
        error_msg = "Não foi possível salvar a nova espécie :/"
        logger.warning(f"Erro ao cadastrar '{especie.nome_popular}', {error_msg}")
        return {"mensagem": error_msg}, 400


@app.get("/especies", tags=[especie_tag], responses={"200": ListagemEspeciesSchema})
def get_especies():
    """Lista todas as espécies cadastradas, com o total de avistamentos de cada uma."""
    logger.debug("Coletando espécies cadastradas")
    session = Session()
    especies = session.query(Especie).order_by(Especie.nome_popular).all()

    if not especies:
        return {"especies": []}, 200

    logger.debug(f"{len(especies)} espécie(s) encontrada(s)")
    return apresenta_especies(especies), 200


@app.get(
    "/especie",
    tags=[especie_tag],
    responses={"200": EspecieViewSchema, "404": ErrorSchema},
)
def get_especie(query: EspecieBuscaSchema):
    """Busca uma espécie a partir do nome popular informado.

    Retorna a espécie e a lista de avistamentos associados a ela.
    """
    nome_popular = query.nome_popular
    logger.debug(f"Buscando espécie '{nome_popular}'")
    session = Session()
    especie = session.query(Especie).filter_by(nome_popular=nome_popular).first()

    if not especie:
        error_msg = "Espécie não encontrada no diário de campo :/"
        logger.warning(f"Erro ao buscar '{nome_popular}', {error_msg}")
        return {"mensagem": error_msg}, 404

    logger.debug(f"Espécie encontrada: '{especie.nome_popular}'")
    return apresenta_especie(especie), 200


@app.delete(
    "/especie",
    tags=[especie_tag],
    responses={"200": EspecieDelSchema, "404": ErrorSchema},
)
def del_especie(query: EspecieBuscaSchema):
    """Remove uma espécie do diário a partir do nome popular informado.

    Os avistamentos vinculados a essa espécie também são removidos.
    """
    nome_popular = query.nome_popular
    logger.debug(f"Removendo espécie '{nome_popular}'")
    session = Session()
    count = session.query(Especie).filter_by(nome_popular=nome_popular).delete()
    session.commit()

    if count:
        logger.debug(f"Espécie removida: '{nome_popular}'")
        return {"mensagem": "Espécie removida", "nome_popular": nome_popular}

    error_msg = "Espécie não encontrada no diário de campo :/"
    logger.warning(f"Erro ao remover '{nome_popular}', {error_msg}")
    return {"mensagem": error_msg}, 404


# Avistamento


@app.post(
    "/avistamento",
    tags=[avistamento_tag],
    responses={"200": EspecieViewSchema, "404": ErrorSchema, "400": ErrorSchema},
)
def add_avistamento(form: AvistamentoSchema):
    """Registra um novo avistamento de campo, vinculado a uma espécie já cadastrada.

    A data do avistamento deve ser enviada no formato DD/MM/AAAA.
    Retorna a espécie atualizada, já com o novo avistamento na lista.
    """
    nome_popular = form.nome_popular
    logger.debug(f"Registrando avistamento para a espécie '{nome_popular}'")
    session = Session()
    especie = session.query(Especie).filter_by(nome_popular=nome_popular).first()

    if not especie:
        error_msg = "Espécie não encontrada no diário de campo :/"
        logger.warning(
            f"Erro ao registrar avistamento para '{nome_popular}', {error_msg}"
        )
        return {"mensagem": error_msg}, 404

    try:
        data_avistamento = _parse_data(form.data_avistamento)
    except ValueError:
        error_msg = "Data inválida. Utilize o formato DD/MM/AAAA."
        logger.warning(
            f"Erro ao registrar avistamento para '{nome_popular}', {error_msg}"
        )
        return {"mensagem": error_msg}, 400

    avistamento = Avistamento(
        local=form.local,
        data_avistamento=data_avistamento,
        observador=form.observador or "",
        quantidade=form.quantidade or 1,
        condicoes_climaticas=form.condicoes_climaticas or "",
    )

    especie.adiciona_avistamento(avistamento)
    session.commit()

    logger.debug(f"Avistamento registrado para '{nome_popular}' em '{form.local}'")
    return apresenta_especie(especie), 200


@app.delete(
    "/avistamento",
    tags=[avistamento_tag],
    responses={"200": AvistamentoDelSchema, "404": ErrorSchema},
)
def del_avistamento(query: AvistamentoBuscaSchema):
    """Remove um avistamento específico a partir do seu id."""
    avistamento_id = query.id
    logger.debug(f"Removendo avistamento #{avistamento_id}")
    session = Session()
    count = session.query(Avistamento).filter(Avistamento.id == avistamento_id).delete()
    session.commit()

    if count:
        logger.debug(f"Avistamento removido #{avistamento_id}")
        return {"mensagem": "Avistamento removido", "id": avistamento_id}

    error_msg = "Avistamento não encontrado :/"
    logger.warning(f"Erro ao remover avistamento #{avistamento_id}, {error_msg}")
    return {"mensagem": error_msg}, 404


# Estatísticas (rota extra, mostra relação entre as duas tabelas)


@app.get("/estatisticas", tags=[estatistica_tag])
def get_estatisticas():
    """Retorna um resumo do diário de campo: total de espécies cadastradas,
    total de avistamentos registrados e a espécie com mais avistamentos.
    """
    session = Session()
    try:
        total_especies = session.query(Especie).count()
        total_avistamentos = session.query(Avistamento).count()

        especie_destaque = (
            session.query(Especie, func.count(Avistamento.id).label("total"))
            .outerjoin(Avistamento, Avistamento.especie == Especie.id)
            .group_by(Especie.id)
            .order_by(func.count(Avistamento.id).desc())
            .first()
        )

        destaque = None
        if especie_destaque and especie_destaque[1] > 0:
            destaque = {
                "nome_popular": especie_destaque[0].nome_popular,
                "total_avistamentos": especie_destaque[1],
            }
    finally:
        session.close()

    logger.debug("Estatísticas calculadas")
    return {
        "total_especies": total_especies,
        "total_avistamentos": total_avistamentos,
        "especie_mais_avistada": destaque,
    }, 200
