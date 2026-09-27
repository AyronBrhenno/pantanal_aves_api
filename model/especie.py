from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from model import Avistamento, Base


class Especie(Base):
    """Representa uma espécie de ave catalogada no diário de campo do Pantanal."""

    __tablename__ = "especie"

    id = Column("pk_especie", Integer, primary_key=True)
    nome_popular = Column(String(140), unique=True, nullable=False)
    nome_cientifico = Column(String(160))
    familia = Column(String(100))
    status_conservacao = Column(String(40), default="Não avaliado")
    data_cadastro = Column(DateTime, default=datetime.now())

    # Relação 1:N -> uma espécie pode ter vários avistamentos registrados.
    # cascade garante que, ao remover a espécie, os avistamentos vinculados
    # também sejam removidos.
    avistamentos = relationship("Avistamento", cascade="all, delete-orphan")

    def __init__(
        self,
        nome_popular: str,
        nome_cientifico: str = "",
        familia: str = "",
        status_conservacao: str = "Não avaliado",
        data_cadastro: datetime | None = None,
    ):
        """
        Cria uma Espécie

        Arguments:
            nome_popular: nome popular pelo qual a espécie é conhecida
            nome_cientifico: nome científico (binômio) da espécie
            familia: família taxonômica da espécie
            status_conservacao: situação de conservação da espécie
            data_cadastro: data em que a espécie foi cadastrada na base
        """
        self.nome_popular = nome_popular
        self.nome_cientifico = nome_cientifico
        self.familia = familia or ""
        self.status_conservacao = status_conservacao or ""

        if data_cadastro:
            self.data_cadastro = data_cadastro
        else:
            self.data_cadastro = datetime.now()

    def adiciona_avistamento(self, avistamento: Avistamento):
        """Associa um novo avistamento de campo a esta espécie."""
        self.avistamentos.append(avistamento)
