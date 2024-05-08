# Documentação do Projeto FastAPI com JWT

Este documento descreve a estrutura e funcionalidades de um projeto FastAPI que utiliza JWT para autenticação.

## Tecnologias Utilizadas

- **FastAPI**: Framework web Python assíncrono de alto desempenho.
- **SQLAlchemy**: ORM para interação com banco de dados.
- **SQLite**: Banco de dados utilizado.
- **Jinja2**: Engine de templates para renderização de páginas HTML.
- **uvicorn**: Servidor ASGI de alto desempenho.

## Estrutura do Projeto

- **main.py**: Arquivo principal da aplicação, onde são definidas as rotas, configuração do banco de dados e JWT.
- **database/database.py**: Configurações do SQLAlchemy e criação da instância do banco de dados.
- **database/models.py**: Define os modelos do banco de dados, no caso, o modelo User.
- **templates/**: Pasta contendo os templates HTML para login, registro e página de erro.

## Funcionalidades

- **Registro de Usuários**: A rota `/register` permite registrar novos usuários, armazenando as informações no banco de dados.
- **Login**: A rota `/login` autentica o usuário com email e senha, gerando um token JWT e armazenando-o em um cookie.
- **CRUD de Usuários**: As rotas `/users`, `/users/{user_id}`, permitem listar, buscar, atualizar e deletar usuários.

## Instruções para Rodar o Projeto

1. **Instalar dependências**: Execute `pip install -r requirements.txt` para instalar as bibliotecas necessárias.
2. **Criar banco de dados**: Execute `python3 main.py create_db` para criar as tabelas no banco de dados SQLite.
3. **Rodar a aplicação**: Execute `python3 main.py` para iniciar o servidor FastAPI.
4. **Acessar a aplicação**: Abra o navegador e acesse [http://localhost:5000/](http://localhost:5000/) para acessar a aplicação e testar as funcionalidades de registro e login de usuários.
5. **Acessar a documentação**: Abra o navegador e acesse [http://localhost:5000/docs](http://localhost:5000/docs) para acessar a documentação das rotas e testar as funcionalidades disponíveis.
6. **Rodar a aplicação com Docker Compose**:
   - Certifique-se de ter o Docker e o Docker Compose instalados.
   - No terminal, navegue até o diretório raiz do projeto onde está localizado o arquivo `docker-compose.yaml`.
   - Execute `docker-compose up --build` para construir e iniciar os containers.