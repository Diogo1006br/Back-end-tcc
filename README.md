
# Título do Projeto

Uma breve descrição sobre o que esse projeto faz e para quem ele é

Agora, o front-end está configurado e pronto para uso.

yaml


---

### BACK-END: Configuração Completa

```markdown
# Configuração do Back-end

Este guia descreve como configurar e executar o projeto de back-end.

---

## Pré-requisitos

Certifique-se de ter os seguintes softwares instalados:

- [Python](https://www.python.org/) (versão recomendada: 3.10 ou superior)
- [pip](https://pip.pypa.io/en/stable/) (gerenciador de pacotes do Python)
- [PostgreSQL](https://www.postgresql.org/) (como banco de dados)

---

## Passo a Passo

### 1. Clonar o Repositório
Clone o repositório do projeto usando o comando abaixo:
```bash
git clone <url-do-repositorio-back-end>
2. Navegar para o Diretório do Projeto
Entre no diretório do projeto clonado:

bash

cd <nome-do-diretorio-clonado>
3. Criar e Ativar um Ambiente Virtual
Crie um ambiente virtual para o projeto:

bash

python -m venv venv
Ative o ambiente virtual:

Windows:
bash

venv\Scripts\activate
Linux/Mac:
bash

source venv/bin/activate
4. Instalar as Dependências
Instale todas as dependências do projeto:

bash

pip install -r requirements.txt
Configuração do Banco de Dados
5. Configurar Variáveis de Ambiente
Crie um arquivo .env ou renomeie o arquivo .env.example, caso exista, e preencha as informações necessárias. Exemplo:

env

SECRET_KEY=sua-chave-secreta-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://usuario:senha@localhost:5432/nome_do_banco
6. Criar o Banco de Dados no PostgreSQL
Certifique-se de que o PostgreSQL está rodando e crie o banco de dados:

sql

CREATE DATABASE nome_do_banco;
7. Rodar as Migrações
Aplique as migrações para configurar o banco de dados:

bash

python manage.py migrate
Executando o Servidor
8. Iniciar o Servidor de Desenvolvimento
Execute o servidor de desenvolvimento:

bash

python manage.py runserver
Acesse o projeto no navegador em: http://localhost:8000.

Rodando Testes
9. Rodar Testes Automatizados
Execute os testes do projeto:

bash

python manage.py test
Comandos Úteis
Ativar o ambiente virtual:

Windows:
bash

venv\Scripts\activate
Linux/Mac:
bash

source venv/bin/activate
Instalar dependências:

bash

pip install -r requirements.txt
Executar migrações:

bash

python manage.py migrate
Iniciar o servidor:

bash

python manage.py runserver
Executar os testes:

bash

python manage.py test
