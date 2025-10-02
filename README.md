# 🎲 Banco Imobiliário - Simulador de Jogo

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://pytest.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simulador de jogos de banco imobiliário com diferentes estratégias de jogadores, desenvolvido em Python com FastAPI.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura](#arquitetura)
- [Instalação e Execução](#instalação-e-execução)
- [Executando os Testes](#executando-os-testes)
- [Uso da API](#uso-da-api)
- [Regras do Jogo](#regras-do-jogo)
- [Estratégias dos Jogadores](#estratégias-dos-jogadores)
- [Estrutura do Projeto](#estrutura-do-projeto)

## 🎯 Sobre o Projeto

Este projeto simula partidas de um jogo similar ao Banco Imobiliário, onde 4 jogadores com diferentes estratégias de comportamento competem para acumular propriedades e dinheiro. O objetivo é determinar qual estratégia é mais eficaz através de múltiplas simulações.

### O Desafio

O desafio consiste em criar um simulador que:

- ✅ Simula partidas completas de banco imobiliário
- ✅ Implementa 4 estratégias diferentes de jogadores
- ✅ Executa múltiplas simulações para análise estatística
- ✅ Fornece uma API REST para acessar as simulações
- ✅ Possui logs detalhados de todas as ações do jogo
- ✅ Inclui testes automatizados completos

## ✨ Características

- 🎮 **4 Estratégias de Jogadores**: Impulsivo, Exigente, Cauteloso e Aleatório
- 🏠 **20 Propriedades**: Tabuleiro com 20 propriedades únicas
- 📊 **Análise Estatística**: Simulação de múltiplos jogos para análise de desempenho
- 🚀 **API REST**: Interface FastAPI com documentação Swagger automática
- 📝 **Sistema de Logs**: Logging detalhado com cores e emojis
- ✅ **Testes Completos**: Cobertura de testes unitários e de integração
- 🐳 **Docker**: Containerização com Docker e Docker Compose
- 🎨 **Código Limpo**: Seguindo princípios SOLID e boas práticas

## 🛠️ Tecnologias Utilizadas

- **Python 3.11** - Linguagem de programação
- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados e serialização
- **Pytest** - Framework de testes
- **Docker** - Containerização
- **Uvicorn** - Servidor ASGI
- **Python Logging** - Sistema de logs customizado

## 🏗️ Arquitetura

O projeto segue os princípios de **Clean Architecture** e **SOLID**:

```
┌─────────────────────────────────────────┐
│           API Layer (FastAPI)            │
│         /game/simulate                   │
│         /game/simulate/multiple          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Service Layer                    │
│    AutoRunner - Game Orchestration       │
│    Logger - Logging System               │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Domain Layer                     │
│    Player - Behavior Strategies          │
│    Property - Game Properties            │
│    Board - Game Board                    │
└──────────────────────────────────────────┘
```

### Padrões de Projeto Utilizados

- **Strategy Pattern**: Diferentes comportamentos de jogadores
- **Singleton Pattern**: Instância única do logger
- **Factory Pattern**: Criação de jogadores e propriedades
- **Dependency Injection**: Injeção de dependências no FastAPI

## 📦 Instalação e Execução

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose (opcional)
- pip (gerenciador de pacotes Python)

### Opção 1: Executar com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/Pissinatti-py/challenge.git
cd challenge

# Construa e inicie os containers
docker-compose up --build

# A API estará disponível em http://localhost:8000
```

### Opção 2: Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/Pissinatti-py/challenge.git
cd challenge

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:

- **URL**: http://localhost:8000
- **Documentação Interativa**: http://localhost:8000/docs
- **Documentação Alternativa**: http://localhost:8000/redoc

## 🧪 Executando os Testes

### Executar Todos os Testes

```bash
# Com Docker
docker-compose exec fastapi-app python -m pytest

# Localmente (com ambiente virtual ativado)
python -m pytest
```

### Executar Testes com Cobertura

```bash
# Gerar relatório de cobertura
python -m pytest --cov=src --cov-report=html --cov-report=term-missing

# Abrir relatório HTML
# Linux/Mac:
open htmlcov/index.html
# Windows:
start htmlcov/index.html
```

### Executar Testes Específicos

```bash
# Testes de um módulo específico
python -m pytest tests/services/test_player.py -v

# Testes de uma classe específica
python -m pytest tests/services/test_player.py::TestPlayerBehaviors -v

# Teste específico
python -m pytest tests/services/test_player.py::TestPlayerBehaviors::test_impulsive_always_buys -v

# Testes por marcadores
python -m pytest -m unit
python -m pytest -m integration
```

### Estrutura de Testes

```
tests/
├── conftest.py                 # Fixtures compartilhadas
├── services/
│   ├── test_player.py         # Testes de jogadores
│   ├── test_property.py       # Testes de propriedades
│   ├── test_board.py          # Testes do tabuleiro
│   └── test_runner.py         # Testes do runner
└── endpoints/
    └── test_game_endpoint.py  # Testes da API
```

## 🔌 Uso da API

### Endpoints Disponíveis

#### 1. Simular um Único Jogo

```bash
curl -X GET "http://localhost:8000/game/simulate"
```

**Resposta:**

```json
{
  "winner": "Impulsivo",
  "total_turns": 245,
  "timeout": false,
  "players": [
    {
      "name": "Impulsivo",
      "behavior": "Impulsivo",
      "balance": 450,
      "properties_owned": ["Avenida Paulista", "Copacabana"],
      "is_active": true,
      "total_assets": 690
    },
    ...
  ],
  "final_standings": [
    {
      "position": 1,
      "name": "Impulsivo",
      "balance": 450,
      "properties_count": 5
    },
    ...
  ]
}
```

#### 2. Simular Múltiplos Jogos

```bash
curl -X GET "http://localhost:8000/game/simulate/multiple?simulations=10"
```

**Resposta:**

```json
{
  "total_simulations": 10,
  "wins_by_behavior": {
    "Impulsivo": 45,
    "Exigente": 20,
    "Cauteloso": 25,
    "Aleatório": 10
  },
  "win_percentages": {
    "Impulsivo": 45.0,
    "Exigente": 20.0,
    "Cauteloso": 25.0,
    "Aleatório": 10.0
  },
  "average_turns": 245.5,
  "timeout_count": 2
}
```

### Usando Python Requests

```python
import requests

# Simular um jogo
response = requests.get("http://localhost:8000/game/simulate")
result = response.json()
print(f"Vencedor: {result['winner']}")
print(f"Turnos: {result['total_turns']}")

# Simular 100 jogos
response = requests.get(
    "http://localhost:8000/game/simulate/multiple",
    params={"simulations": 100}
)
stats = response.json()
print(f"Estatísticas: {stats['win_percentages']}")
```

## 🎲 Regras do Jogo

### Tabuleiro

- **20 propriedades** em sequência
- Cada propriedade tem um **custo de venda** e um **valor de aluguel**
- Propriedades podem ser **compradas** quando disponíveis

### Jogadores

- Cada jogador inicia com **$300**
- Jogam em turnos, rolando um **dado de 6 faces**
- Movem-se pelo tabuleiro baseado no resultado do dado
- Ao completar uma volta, ganham **$100** de bônus

### Compra de Propriedades

- Jogadores podem comprar propriedades **disponíveis**
- Devem ter **dinheiro suficiente** para a compra
- A decisão de compra depende da **estratégia do jogador**

### Pagamento de Aluguel

- Ao parar em propriedade de outro jogador, deve **pagar aluguel**
- O valor do aluguel vai para o **dono da propriedade**
- Jogador que fica com **saldo negativo** vai à **falência**

### Falência

- Jogador com **saldo negativo** perde o jogo
- Suas propriedades voltam a ficar **disponíveis**
- Não participa mais das rodadas

### Vitória

- Jogo termina quando resta **apenas um jogador** ativo
- Ou quando atinge o **limite de 1000 turnos** (timeout)
- Vencedor é o jogador com **saldo positivo** remanescente

## 🧠 Estratégias dos Jogadores

### 1. 🚀 Impulsivo

```python
Compra qualquer propriedade sobre a qual parar
```

- **Estratégia**: Agressiva
- **Vantagem**: Acumula propriedades rapidamente
- **Desvantagem**: Pode ficar sem dinheiro

### 2. 💎 Exigente

```python
Compra apenas se aluguel > $50
```

- **Estratégia**: Seletiva
- **Vantagem**: Propriedades de alto retorno
- **Desvantagem**: Pode perder boas oportunidades

### 3. 🛡️ Cauteloso

```python
Compra apenas se sobrar $80+ após a compra
```

- **Estratégia**: Defensiva
- **Vantagem**: Sempre mantém reserva financeira
- **Desvantagem**: Menos propriedades

### 4. 🎰 Aleatório

```python
Compra com 50% de probabilidade
```

- **Estratégia**: Imprevisível
- **Vantagem**: Equilibrado
- **Desvantagem**: Inconsistente

## 📁 Estrutura do Projeto

```
challenge/
├── src/
│   ├── api/
│   │   └── routes/
│   │       └── game.py              # Rotas da API
│   ├── models/
│   │   ├── player.py                # Modelo de Jogador
│   │   ├── property.py              # Modelo de Propriedade
│   │   └── board.py                 # Modelo do Tabuleiro
│   ├── services/
│   │   ├── runner.py                # Orquestrador do jogo
│   │   └── logging.py               # Sistema de logs
│   ├── schemas/
│   │   └── __init__.py              # Schemas Pydantic
│   └── main.py                      # Aplicação FastAPI
├── tests/
│   ├── conftest.py                  # Fixtures pytest
│   ├── services/
│   │   ├── test_player.py
│   │   ├── test_property.py
│   │   ├── test_board.py
│   │   └── test_runner.py
│   └── endpoints/
│       └── test_game_endpoint.py
├── logs/                            # Logs da aplicação
├── docker-compose.yml               # Configuração Docker
├── Dockerfile                       # Imagem Docker
├── requirements.txt                 # Dependências
├── pytest.ini                       # Configuração pytest
└── README.md                        # Este arquivo
```

## 📊 Resultados e Análises

Para analisar qual estratégia é mais eficaz, execute múltiplas simulações:

```bash
# Via API
curl -X GET "http://localhost:8000/game/simulate/multiple?simulations=10"

# Via Python
python -c "
from src.services.runner import AutoRunner

results = {'Impulsivo': 0, 'Exigente': 0, 'Cauteloso': 0, 'Aleatório': 0}

for _ in range(10):
    runner = AutoRunner()
    result = runner.run(show_status_every=0)
    results[result.winner.name] += 1

for player, wins in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f'{player}: {wins} vitórias ({wins/10:.1f}%)')
"
```

## 🐛 Debug e Logs

Os logs são salvos em `logs/game.log` e incluem:

- 🎮 Início e fim de jogo
- 🎲 Rolagem de dados
- 🏠 Compra de propriedades
- 💰 Pagamento de aluguéis
- 💸 Falências
- 🏆 Vencedor

Exemplo de log:

```
14:23:45 | ℹ️  INFO | 🎮 Novo jogo iniciado com 4 jogadores
14:23:45 | ℹ️  INFO | ⏱️  Turno 1 - Vez de Impulsivo
14:23:45 | 🔍 DEBUG | 🎲 Impulsivo tirou 6 no dado
14:23:45 | ℹ️  INFO | 🏠 Impulsivo comprou 'Jardins' por $130
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Marcus Vinicius

## 🙏 Agradecimentos

- FastAPI pela excelente documentação
- Comunidade Python pelas bibliotecas incríveis
- Todos que contribuíram com feedback e sugestões

---

⭐ **Se este projeto foi útil, considere dar uma estrela!**

📧 **Contato**: [Email](marcusandrade.37@gmail.com)

🔗 **Links Úteis**:

- [Documentação FastAPI](https://fastapi.tiangolo.com)
- [Pytest Documentation](https://docs.pytest.org)
- [Docker Documentation](https://docs.docker.com)
