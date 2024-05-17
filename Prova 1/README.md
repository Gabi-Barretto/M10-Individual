# Documentação do Projeto FastAPI e Insomnia

Este documento descreve a estrutura e funcionalidades de um projeto FastAPI que pode ser testado via collection do Insominia disponível no repositótio em [Collection](https://github.com/Gabi-Barretto/M10-Individual/tree/main/Prova%201/Collection).

## Tecnologias Utilizadas

- **FastAPI**: Framework web Python assíncrono de alto desempenho.
- **SQLAlchemy**: ORM para interação com banco de dados.
- **SQLite**: Banco de dados utilizado.
- **uvicorn**: Servidor ASGI de alto desempenho.
- **Docker**: Conteinerizar a aplicação

## Estrutura do Projeto

- **main.py**: Arquivo principal da aplicação, onde são definidas as rotas, configuração do banco de dados.
- **database/database.py**: Configurações do SQLAlchemy e criação da instância do banco de dados.
- **database/models.py**: Define os modelos do banco de dados, no caso, o modelo User.

## Funcionalidades

- **Registro de pedidos**: A rota `/novo` permite registrar novos pedidos, armazenando as informações no banco de dados.
- **CRUD de pedidos**: As rotas `/pedidos`, `/pedidos/{pedido_id}`, permitem listar, buscar, atualizar e deletar usuários.

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