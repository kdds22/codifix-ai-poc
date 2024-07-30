# Fix.Ai `Code`

Bem vindo ao **Fix.Ai `Code`**, com tecnologia da [crewAI](https://crewai.com). 

## Instalação

Certifique-se de ter o __Python >=3.10 <=3.13__ instalado no seu sistema.

> No diretório do projeto, abra o terminal e siga as instruções abaixo...

Primeiro, crie um novo ambiente (_environment_):

```bash
python3 -m venv .venv
```
e ative-o...
```bash
source .venv/bin/activate
```


Então... Este projeto utiliza o [Poetry](https://python-poetry.org/) para gerenciamento de dependências e manipulação de pacotes, oferecendo uma experiência de configuração e execução sem complicações.

Então, se ainda não o tem, instale o **Poetry**:

```bash
pip install poetry
```

Agora, instale as dependências:
1. Primeiro bloqueie as dependências
```bash
poetry lock
```
2. E agora... instale-as:
```bash
poetry install
```
---
## Customização

### Configurando variáveis de ambiente `.env`
Crie o arquivo `.env` na raiz do projeto e insira as variáveis:

**Variáveis:**
- `OPENAI_API_KEY`
- `OPENAI_MODEL_NAME` 
- `GOOGLE_APPLICATION_CREDENTIALS`  
- `GIT_AZURE_TOKEN`
- `GIT_AZURE_REPO` 
- `GIT_AZURE_SQUAD`

---

#### Requisitos

##### OPENAI_API_KEY:
> Token usado para fazer usar o GPT da OpenAI

##### OPENAI_MODEL_NAME: 
> Nome do LLM usado
> - ex.: `OPENAI_MODEL_NAME="gpt-3.5-turbo"`

##### GOOGLE_APPLICATION_CREDENTIALS: 
> Caminho do arquivo JSON com as cofigurações de conexão com o BigQuery
> - Google Cloud -> IAM & Admin -> Service Account -> Keys -> JSON
>   - Assim como o Token do Azure, salve o JSON em um lugar seguro, caso perca, terá de criar uma nova chave.

##### GIT_AZURE_TOKEN: 
> Token de acesso do Azure para clonar o repositório
> - No azure, vai em __Configurações de usuário__ (User Settings)
> - Depois em __Tokens de acesso pessoal__ (Personal access tokens)
> - Click em `+ Novo Token`
>     - Defina um nome e organização
>     - Selecione `Full access`, na seção `Scopes`
> - Salve o TOKEN
>     - (o azure não permite visualizar após fechar o modal)

##### GIT_AZURE_REPO: 
> Nome do Repositório no azure
> - Ex.: `GIT_AZURE_REPO="Havan.RFID.Agility.Abastecimento"`

##### GIT_AZURE_SQUAD: 
> Nome da SQUAD onde está armazenado o repositório
> - Ex.: `TRON`
>     - `GIT_AZURE_SQUAD="https://TOKEN@dev.azure.com/HavanLabs/TRON/_git/Havan.RFID.Agility.Abastecimento"`

##### WEBHOOK_URL: 
> URL do Webhook criado para notificar no Microsoft Teams

---

## Organização
- Modifique `src/codifix_ai/config/agents.yaml` para ajustar os agentes
- Modifique `src/codifix_ai/config/tasks.yaml` para ajustar as tarefas
- Modifique `src/codifix_ai/main.py` para adicionar sua lógica e argumentos
- Modifique `src/codifix_ai/tools/custom_tools.py` para customizar suas ferramentas
- Modifique `src/codifix_ai/models/custom_models.py` para customizar **tipos** dos objetos I/O
---

## Executando o projeto

Para iniciar sua equipe de agentes de IA e realizar as tarefas, execute o seguinte comando:

```bash
poetry run fix_ai_code
```

---
## Entendendo a equipe de agentes

A equipe fix_ai é composta por vários agentes de IA, cada um com funções, objetivos e ferramentas exclusivos. Esses agentes colaboram em uma série de tarefas, definidas em `config/tasks.yaml`, aproveitando suas habilidades coletivas para atingir objetivos complexos. O arquivo `config/agents.yaml` descreve as capacidades e configurações de cada agente da sua equipe.
No momento os agentes estão customizados para aplicações Android (Kotlin). 
Utilizando o [Google BigQuery](https://console.cloud.google.com/bigquery) para buscar os LOGs dos erros. 
O [Azure DevOps](https://dev.azure.com/) para acessar os repositórios. 
O [Microsoft Teams](https://teams.microsoft.com/v2/) para notificar via `Webhook`.

---

## Próximos passos
- Automatizar Pull Request com a sugestão dos agentes
- Engenharia de Prompt para Swift/Objective-C
- Ajustes reportados pelo SonarQube
- Ajustes reportados pelo DataDog
- Utilizar o lang-chain para customizar diferentes modelos (LLM)
    - Azure
    - Ollama
    - LM Studio
    - Groq

