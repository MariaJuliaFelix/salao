from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import criar_tabela


from app.routes import clientes, servicos, agendamentos

criar_tabela()

app = FastAPI()

# 🔹 AGORA APONTA PARA A PASTA CORRETA (fora do app)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔹 TEMPLATES TAMBÉM FORA DO app
templates = Jinja2Templates(directory="templates")


# 🔹 ROTA PRINCIPAL
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 🔹 ROTAS
app.include_router(clientes.router, prefix="/clientes")
app.include_router(servicos.router, prefix="/servicos")
app.include_router(agendamentos.router, prefix="/agendamentos")