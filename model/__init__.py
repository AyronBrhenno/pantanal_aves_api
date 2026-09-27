from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.avistamento import Avistamento
from model.especie import Especie

db_path = "database/"
# Verifica se o diretório não existe
if not os.path.exists(db_path):
    # então cria o diretório
    os.makedirs(db_path)

# url de acesso ao banco (SQLite local). O arquivo é criado automaticamente
# pelo próprio driver do SQLite assim que a primeira conexão é aberta.
db_url = 'sqlite:///%s/pantanal_aves.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# instancia um criador de sessão com o banco
Session = sessionmaker(bind=engine)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
