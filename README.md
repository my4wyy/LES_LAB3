# Laboratório 03 - Code Review no GitHub

## Pré-requisitos:
- Python 3.7+
- Conta no GitHub (para aumentar limite de API)

## Configuração do ambiente:

Instale as dependências:
pip install requests pandas

## Como executar:

1. Execute o script para buscar os repositórios:
cd scripts
python 01_fetch_repos.py

2. Execute o script para buscar os Pull Requests:
python 02_fetch_prs.py

## Estrutura de pastas:
- data/repositories.csv: Lista dos 200 repositórios mais populares
- data/pull_requests.csv: Dataset completo dos PRs coletados
- scripts/: Contém os scripts de coleta
- venv/: Ambiente virtual Python (não versionar)

## Observações:
- A coleta pode demorar várias horas devido aos limites da API do GitHub
- Recomendado usar token de autenticação do GitHub para evitar limites de rate limiting