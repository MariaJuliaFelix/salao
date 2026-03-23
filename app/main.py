from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import criar_tabelas
from app.routes import clientes, servicos, agendamentos, gerencial

criar_tabelas()

app = FastAPI(title="Sistema de Agendamento para Salão")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(servicos.router, prefix="/servicos", tags=["Serviços"])
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"])
app.include_router(gerencial.router, prefix="/gerencial", tags=["Gerencial"])