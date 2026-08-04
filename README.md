# MinMax-Tic-Tac-Toe
Projeto de implementação do algoritmo MinMax para o jogo da velha (Tic-Tac-Toe) em Python.

<!-- TABLE OF CONTENTS -->

## Tabela de Conteúdo

- [MinMax-Tic-Tac-Toe](#minmax-tic-tac-toe)
  - [Tabela de Conteúdo](#tabela-de-conteúdo)
  - [Sobre o Projeto](#sobre-o-projeto)
    - [Feito Com](#feito-com)
  - [Começando](#começando)
    - [Pré-requisitos](#pré-requisitos)
    - [Estrutura de Arquivos](#estrutura-de-arquivos)
    - [Instalação](#instalação)
    - [Configuração do Ambiente Virtual](#configuração-do-ambiente-virtual)
      - [Linux/Ubuntu](#linuxubuntu)
      - [Windows (Command Prompt)](#windows-command-prompt)
    - [Execução do Código](#execução-do-código)
      - [Linux/Ubuntu](#linuxubuntu-1)
      - [Windows (Command Prompt)](#windows-command-prompt-1)
    - [Execução dos Testes](#execução-dos-testes)
    - [Edição](#edição)

<!-- ABOUT THE PROJECT -->

## Sobre o Projeto

Este projeto consiste na implementação do algoritmo **Minimax** aplicado ao jogo da velha (Tic-Tac-Toe) utilizando Python. O objetivo é desenvolver uma inteligência artificial capaz de escolher sempre a melhor jogada possível dentro da profundidade
observada, garantindo que o jogador controlado pelo algoritmo tome as melhores decisões durante o jogo.

### Feito Com

Este projeto foi desenvolvido utilizando as seguintes tecnologias:

- Python 3.12+
- Pytest
- Ruff

<!-- GETTING STARTED -->

## Começando

Para começar a utilizar este projeto, é necessário ter alguns pré-requisitos de ambiente.

### Pré-requisitos

1. A utilização do ambiente requer a instalação do Python 3.12 ou superior. Certifique-se de que o Python esteja instalado em seu sistema antes de prosseguir.
2. Utiliza-se Git para clonar o repositório. Caso não tenha o Git instalado, o usuário pode baixar o projeto como um arquivo ZIP, através da url do repositório, e descompactá-lo em seu sistema.

### Estrutura de Arquivos

A estrutura de arquivos está da seguinte maneira:

```bash
minmax-tic-tac-toe/
  ├── src/
  │   ├── tictactoe/
  │   │   ├── ai/
  │   │   │   └── minmax.py
  │   │   │
  │   │   ├── game/
  │   │   │   ├── board.py
  │   │   │   ├── match.py    
  │   │   │   └── player_mark.py
  │   │   │        
  │   │   ├── ui/
  │   │   │   ├── pygame_ui.py
  │   │   │   └── console.py 
  │   │   │
  │   │   └── utils/
  │   │
  ├── tests/
  │   ├── test_board.py
  │   └── test_minmax.py
  │   └── test_match.py  
  │
  ├── .gitignore
  ├── LICENSE
  ├── pyproject.toml
  └── README.md
```

### Instalação

1. Para instalar e utilizar esse projeto, basta clonar o repositório:

```bash
git clone <REPO_URL>
```

2. Certifique-se de que você está no diretório do projeto:

```bash
cd minmax-tic-tac-toe
```

### Configuração do Ambiente Virtual

Crie e ative um ambiente virtual.

#### Linux/Ubuntu

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -e ".[dev]"
```

#### Windows (Command Prompt)

```cmd
python -m venv .venv

.venv\Scripts\activate

pip install -e ".[dev]"
```

O comando acima instala o projeto em modo editável juntamente com todas as dependências de desenvolvimento definidas no arquivo `pyproject.toml`.

### Execução do Código

Após ativar o ambiente virtual, execute:

#### Linux/Ubuntu

```bash
source .venv/bin/activate

python -m tictactoe
```

#### Windows (Command Prompt)

```cmd
.venv\Scripts\activate

python -m tictactoe
```

### Execução dos Testes

Para executar todos os testes:

```bash
pytest
```

Para exibir informações mais detalhadas:

```bash
pytest -v
```

Para gerar um relatório de cobertura:

```bash
pytest --cov=src --cov-report=term-missing
```

### Edição

Descrição dos principais diretórios do projeto:

- **src/**
  Código-fonte da aplicação.

- **src/tictactoe/ai/**
  Implementação dos algoritmos de inteligência artificial, como o Minimax.

- **src/tictactoe/game/**
  Implementação da lógica do jogo, incluindo o tabuleiro e as regras.

- **src/tictactoe/ui/**
  Interface responsável pela interação com o usuário.

- **src/tictactoe/utils/**
  Classes e funções auxiliares utilizadas pelo projeto.

- **tests/**
  Testes automatizados utilizando Pytest.

- **pyproject.toml**
  Configuração do projeto, metadados e dependências.

- **README.md**
  Documentação do projeto.
