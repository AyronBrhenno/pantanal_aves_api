from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from model import Base


class Avistamento(Base):
    """Representa o registro de campo de um avistamento de uma espécie,
    feito por um observador em um local e data específicos.
    """

    __tablename__ = "avistamento"

    id = Column("pk_avistamento", Integer, primary_key=True)
    local = Column(String(140), nullable=False)
    observador = Column(String(100))
    quantidade = Column(Integer, default=1)
    condicoes_climaticas = Column(String(80))
    data_avistamento = Column(DateTime, nullable=False)
    data_insercao = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Chave estrangeira que relaciona o avistamento à espécie observada
    especie = Column(Integer, ForeignKey("especie.pk_especie"), nullable=False)

    def __init__(
        self,
        local: str,
        data_avistamento: datetime,
        observador: str = "",
        quantidade: int = 1,
        condicoes_climaticas: str = "",
        data_insercao: datetime | None = None,
    ):
        """
        Cria um registro de Avistamento

        Arguments:
            local: local onde a ave foi avistada
            data_avistamento: data em que o avistamento ocorreu em campo
            observador: nome de quem avistou a ave
            quantidade: número de indivíduos observados
            condicoes_climaticas: clima no momento do avistamento
            data_insercao: data em que o registro foi inserido na base
        """
        self.local = local
        self.data_avistamento = data_avistamento
        self.observador = observador
        self.quantidade = quantidade
        self.condicoes_climaticas = condicoes_climaticas

        if data_insercao:
            self.data_insercao = data_insercao
