from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import agendamentos, clientes, servicos

app = FastAPI()

# static (css/js)
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates
templates = Jinja2Templates(directory="templates")

# rotas
app.include_router(agendamentos.router)
app.include_router(clientes.router)
app.include_router(servicos.router)