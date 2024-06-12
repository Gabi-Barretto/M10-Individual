### Documentação do Projeto FastAPI com JWT, Flutter e RabbitMQ

Este documento descreve a estrutura e funcionalidades de um projeto FastAPI que utiliza JWT para autenticação, Flutter para sua UI, e RabbitMQ para salvar logs. Tudo em microserviços;

### [*Vídeo Demonstrativo*](https://drive.google.com/file/d/1Vh3TFzF9M7p_2Tzg7zVJIRP1NTqEElaN/view?usp=sharing)

## Tecnologias Utilizadas

- **FastAPI**: Framework web Python assíncrono de alto desempenho.
- **SQLAlchemy**: ORM para interação com banco de dados.
- **SQLite**: Banco de dados utilizado.
- **Jinja2**: Engine de templates para renderização de páginas HTML.
- **uvicorn**: Servidor ASGI de alto desempenho.
- **RabbitMQ**: Sistema de mensageria para gerenciamento de logs.

## Estrutura do Projeto

- **main.py**: Arquivo principal da aplicação, onde são definidas as rotas, configuração do banco de dados, JWT e RabbitMQ.
- **database/database.py**: Configurações do SQLAlchemy e criação da instância do banco de dados.
- **database/models.py**: Define os modelos do banco de dados, no caso, o modelo User.
- **templates/**: Pasta contendo os templates HTML para login, registro e página de erro.

## Funcionalidades

- **Registro de Usuários**: A rota `/register` permite registrar novos usuários, armazenando as informações no banco de dados.
- **Login**: A rota `/login` autentica o usuário com email e senha, gerando um token JWT e armazenando-o em um cookie.
- **CRUD de Usuários**: As rotas `/users`, `/users/{user_id}`, permitem listar, buscar, atualizar e deletar usuários.
- **Log de Ações**: As rotas `/send-log` e `/receive-log` permitem o envio e recebimento de logs via RabbitMQ, o mesmo método chamado nesses endpoints e foi aplicado nas rotas de cadastro e login.

![Rabbit Existe](./Mídia/image.png)

## Instruções para Rodar o Backend

0. **Utilize do diretório**: [Ponderada 3](https://github.com/Gabi-Barretto/M10-Individual/tree/main/Ponderada%203), para rodar o backend.
1. **Acessar docs**: [User](http://localhost:8001/docs), [Todo](http://localhost:8002/docs), [Log](http://localhost:8003/docs), [Image Processing](http://localhost:8004/docs)
7. **Rodar a aplicação com Docker Compose**:
   - Certifique-se de ter o Docker e o Docker Compose instalados.
   - No terminal, navegue até o diretório raiz do projeto onde está localizado o arquivo `docker-compose.yaml`.
   - Execute `docker-compose up --build` para construir e iniciar os containers.

## Instruções para Rodar o Frontend

1. **Abra o Android Studio**: Inicie o Android Studio e aguarde até que ele termine de carregar e utilize do diretório [Ponderada 2](https://github.com/Gabi-Barretto/M10-Individual/tree/main/Ponderada%202).

2. **Importe o Projeto**:
   - No menu inicial, escolha 'Open an Existing Project' e navegue até a pasta onde você clonou o seu projeto Flutter.
   - Selecione a pasta do projeto e clique em 'OK' para abrir o projeto no Android Studio.

3. **Configure o Emulador Android**:
   - Vá para 'AVD Manager' (Android Virtual Device Manager) no menu 'Tools' > 'AVD Manager'.
   - Clique em 'Create Virtual Device...' e selecione um dispositivo (por exemplo, Pixel 5).
   - Escolha uma imagem do sistema (recomenda-se usar a última versão do Android API que é compatível com seu aplicativo) e finalize a criação do emulador.

4. **Execute o Emulador**:
   - Inicie o emulador criado clicando no botão 'play' ao lado do dispositivo virtual na lista do AVD Manager.

5. **Execute o Aplicativo Flutter**:
   - No Android Studio, certifique-se de que o nome do seu dispositivo emulador está selecionado na barra de ferramentas.
   - Clique no ícone 'Run' (o ícone de um triângulo verde) para compilar o projeto e instalar o aplicativo no emulador.
   - Aguarde até que o aplicativo seja lançado no emulador.

6. **Interagindo com o Aplicativo**:
   - O aplicativo deve agora estar em execução no emulador. Você pode interagir com ele como faria em um dispositivo físico.
   - Teste as funcionalidades implementadas, como as telas de login e registro, e verifique se as transições para outras páginas estão funcionando conforme esperado.

7. **Depuração e Logs**:
   - Utilize a janela 'Logcat' no Android Studio para ver os logs de execução e mensagens de erro. Isso pode ajudar na depuração de problemas que ocorrem durante a execução do aplicativo.