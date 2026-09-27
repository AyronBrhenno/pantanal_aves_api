# API — Diário de Aves do Pantanal

## Descrição

API REST desenvolvida em **Python** com **Flask** (via `flask-openapi3`) para apoiar um
diário de campo de observação de aves do Pantanal mato-grossense. A aplicação permite
cadastrar **espécies** de aves e registrar **avistamentos** de campo vinculados a cada
espécie (local, data, observador, quantidade e condições climáticas), além de consultar
estatísticas gerais do diário.

Este projeto é um MVP (Minimum Viable Product) desenvolvido como atividade da disciplina
de Desenvolvimento Full Stack Básico, explorando as *key constraints* do modelo REST
propostas por Roy Fielding (separação cliente/servidor, interface uniforme, sistema em
camadas, ausência de estado e código sob demanda).

## Modelo de dados

- **Espécie**: `nome_popular`, `nome_científico`, `família`, `status_conservacao`.
- **Avistamento**: `local`, `data_avistamento`, `observador`, `quantidade`,
  `condições_climáticas` — vinculado a uma espécie (relação 1:N).

## Rotas disponíveis

| Método | Rota            | Descrição                                              |
|--------|-----------------|---------------------------------------------------------|
| GET    | `/`             | Redireciona para a documentação (Swagger)               |
| POST   | `/especie`      | Cadastra uma nova espécie                                |
| GET    | `/especies`     | Lista todas as espécies cadastradas                      |
| GET    | `/especie`      | Busca uma espécie pelo nome popular (com avistamentos)   |
| DELETE | `/especie`      | Remove uma espécie (e seus avistamentos)                 |
| POST   | `/avistamento`  | Registra um avistamento vinculado a uma espécie          |
| DELETE | `/avistamento`  | Remove um avistamento pelo id                             |
| GET    | `/estatisticas` | Retorna totais e a espécie mais avistada                 |

## Instruções de instalação

### 1. Pré-requisitos

- Python 3.9+ instalado
- `pip` disponível no terminal

### 2. Clonar o repositório

```bash
git clone https://github.com/AyronBrhenno/pantanal-aves-api.git
cd pantanal-aves-api
```

### 3. Criar e ativar um ambiente virtual

```bash
python -m venv venv
```

- **Windows:** `venv\Scripts\activate`
- **Linux/macOS:** `source venv/bin/activate`

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar a API

```bash
flask run --host 0.0.0.0 --port 5000
```

A API ficará disponível em `http://127.0.0.1:5000`. O banco SQLite é criado
automaticamente na primeira execução, na pasta `database/`.

### 6. Acessar a documentação (Swagger)

Com a API rodando, acesse `http://127.0.0.1:5000/openapi` no navegador para explorar e
testar todas as rotas interativamente.

## Observação

Este backend foi feito para ser consumido pelo projeto de front-end
**pantanal-aves-front**, disponível em um repositório separado.
