# Documentação do Projeto Flask com JWT e Swagger

Este documento descreve a estrutura e funcionalidades de um projeto Flask que utiliza JWT para autenticação e Swagger para documentação da API.

## Tecnologias Utilizadas

- **Flask**: Framework web Python.
- **Flask-JWT-Extended**: Extensão para gerenciamento de JWT.
- **Flasgger**: Extensão para integração com Swagger.
- **SQLAlchemy**: ORM para interação com banco de dados.
- **SQLite**: Banco de dados utilizado.

## Estrutura do Projeto

- **main.py**: Arquivo principal da aplicação, onde são definidas as rotas, configuração do banco de dados, JWT e Swagger.
- **database/database.py**: Configurações do SQLAlchemy e criação da instância do banco de dados.
- **database/models.py**: Define os modelos do banco de dados, no caso, o modelo User.
- **templates/**: Pasta contendo os templates HTML para login, registro, conteúdo e página de erro.
- **yamls/**: Pasta contendo os arquivos YAML para documentação da API com Swagger.

## Funcionalidades

- **Registro de Usuários**: A rota `/register` permite registrar novos usuários, armazenando as informações no banco de dados.
- **Login**: A rota `/login` autentica o usuário com email e senha, gerando um token JWT e armazenando-o em um cookie.
- **CRUD de Usuários**: As rotas `/users`, `/users/<id>`, permitem listar, buscar, atualizar e deletar usuários.
- **Conteúdo Protegido**: A rota `/content` exibe conteúdo restrito a usuários autenticados.

## Instruções para Rodar o Projeto

1. **Instalar dependências**: Em **/src**. Execute `pip install -r requirements.txt` para instalar as bibliotecas necessárias.
2. **Criar banco de dados**: Em **/src**. Execute `python3 main.py create_db` para criar as tabelas no banco de dados SQLite.
3. **Rodar a aplicação**: Em **/src**. Execute `python3 main.py` para iniciar o servidor Flask.
4. **Acessar a documentação**: Abra o navegador e acesse [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/) para visualizar a documentação da API gerada pelo Swagger.

## Configurando o Insomnia

- **Importar Coleção**: Baixe o arquivo de coleção do Insomnia (geralmente com extensão .json) fornecido para o projeto. No Insomnia, clique em "Import/Export" e selecione "Import Data". Escolha o arquivo de coleção baixado.
- **Configurar Ambiente**: Se necessário, configure variáveis de ambiente (JSON com a indicação da variável ex. "id": 1) no Insomnia para definir URLs base, tokens de autenticação ou outros parâmetros usados nas requisições.
- **Enviar Requisições**: Utilize a interface do Insomnia para enviar requisições para as diferentes rotas da API, seguindo a documentação fornecida pelo Swagger e os exemplos na coleção importada.

## Observações

- O arquivo de coleção do Insomnia pode conter exemplos de requisições com valores pré-preenchidos. Adapte esses valores conforme necessário.
- Verifique se a porta utilizada pela aplicação Flask (padrão 5000) coincide com a configuração do ambiente no Insomnia.
- A documentação Swagger, acessível em `/apidocs/`, oferece detalhes sobre os parâmetros, respostas esperadas e códigos de status de cada rota.

Com essas instruções, você poderá executar o projeto e explorar a API utilizando o Insomnia, facilitando o teste e a interação com as funcionalidades.