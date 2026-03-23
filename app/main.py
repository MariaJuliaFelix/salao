from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# IMPORTANDO AS ROTAS
from app.routes import clientes, servicos, agendamentos

app = FastAPI()

# CONFIGURAÇÃO DE ARQUIVOS ESTÁTICOS (CSS e JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# CONFIGURAÇÃO DOS TEMPLATES (HTML)
templates = Jinja2Templates(directory="app/templates")


# ROTA PRINCIPAL (HOME)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# INCLUINDO AS ROTAS
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(servicos.router, prefix="/servicos", tags=["Serviços"])
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"])