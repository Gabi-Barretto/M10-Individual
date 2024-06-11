
from fastapi import FastAPI

app = FastAPI()

# Importar rotas
from . import routes
