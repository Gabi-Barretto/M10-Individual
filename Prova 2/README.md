### Documentação do Projeto FastAPI com JWT, Flutter e RabbitMQ

Este documento descreve a estrutura e funcionalidades de um projeto FastAPI com logs persistidos no diretorio /log e insominia. Por algum motivo os logs nao estavam persistindo no arquivo, mas o professor poderá ver que alógica esta correta para fazer tal.

## Tecnologias Utilizadas

- **FastAPI**: Framework web Python assíncrono de alto desempenho.
- **NGINX**: Gateway.
- **uvicorn**: Servidor ASGI de alto desempenho.

## Estrutura do Projeto

- **main.py**: Arquivo principal da aplicação, onde são definidas as rotas.

## Funcionalidades

- **Registro de blogs**: A rota `/blog` permite registrar novos blogs, armazenando as informações no banco de dados.
- **CRUD de blogs**: As rotas `/blog`, `/blog/{user_id}`, permitem listar, buscar, atualizar e deletar blogs.
- **Log de Ações**: Os logs acima de warning são salvos no arquivo no diretorio logs, dentro de src.

## Instruções para Rodar o Backend

0. **Utilize do diretório**: [Prova 2](https://github.com/Gabi-Barretto/M10-Individual/tree/main/Prova%202), para rodar o backend.
1. **Acessar docs**: [Blog](http://localhost:8001/docs)
2. **Testar com Insominia**: Utilize do arquivo no diretorio Insominia para testar as rotas. Você deve atualizar manualmente o ID do blog em questão nas rotas by Id! 
7. **Rodar a aplicação com Docker Compose**:
   - Certifique-se de ter o Docker e o Docker Compose instalados.
   - No terminal, navegue até o diretório raiz do projeto onde está localizado o arquivo `docker-compose.yaml`.
   - Execute `docker-compose up --build` para construir e iniciar os containers.
