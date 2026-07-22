from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import status
import services
import random

app = FastAPI()

templates = Jinja2Templates(directory="templates")

codigo_rec = None

usuario_logado = None

banco_dados_senhas = {
    "homer": ""
}

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.post("/login")
def login(
    request: Request,
    usuario: str = Form(...),
    senha: str = Form(...)
):  
    global usuario_logado
    
    usuario_logado = None
    salt = None
    
    if banco_dados_senhas[usuario]:
        salt_hex = banco_dados_senhas[usuario].split("$")[2]
        salt = bytes.fromhex(salt_hex)

    string_registro_banco = services.cript_senha(senha, salt)

    if not banco_dados_senhas[usuario]:
        banco_dados_senhas[usuario] = string_registro_banco
    
    if banco_dados_senhas[usuario] == string_registro_banco:
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    
    else:
        return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={"erro_login":"Erro"}
            )


@app.get('/trocar-senha')
def trocar_senha(request: Request):
    global usuario_logado
    
    return templates.TemplateResponse(
        request=request,
        name="trocar-senha.html",
        context={"usuario": usuario_logado or ""}
    )

@app.post('/trocar-senha')
def troca_senha_post(
    request: Request,
    usuario: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str=Form(...)
    ):

    if (usuario in banco_dados_senhas):
        if(senha == confirmar_senha):
            string_registro_banco = services.cript_senha(senha)
            banco_dados_senhas[usuario] = string_registro_banco
            print("Senha Trocada")
            return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse(
                        request=request,
                        name="trocar-senha.html",
                        context={"erro_login":"Senhas Diferentes!"}
                        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="trocar-senha.html",
            context={"erro_login":"Usuario não existe!!!"}
            )
        
@app.get('/esqueci-senha')
def esqueci_senha(request: Request):
        return templates.TemplateResponse(
        request=request,
        name="esqueci-senha.html"
    )
        
@app.post('/esqueci-senha')
def esqueci_senha_post(
    request: Request,
    usuario: str = Form(...)
):
    global codigo_rec, usuario_logado
    
    if(usuario in banco_dados_senhas):
        codigo_rec = f'{random.randint(111111,999999)}'
        print(codigo_rec)
        usuario_logado = usuario
        return RedirectResponse(url="/valida-codigo", status_code=status.HTTP_303_SEE_OTHER)
    else:
         return templates.TemplateResponse(
            request=request,
            name="esqueci-senha.html",
            context={"erro_login":"Usuario não existe!!!"}
            )
    
@app.get('/valida-codigo')
def valida_codigo(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="valida-codigo.html",
        context={"usuario": usuario_logado}
    )
    
    
@app.post('/valida-codigo')
def valida_codigo_post(
    request: Request,
    codigo: str= Form(...)
):
    if(codigo == codigo_rec):
        return RedirectResponse(url="/trocar-senha", status_code=status.HTTP_303_SEE_OTHER)
    else:
         return templates.TemplateResponse(
                    request=request,
                    name="esqueci-senha.html",
                    context={"erro_login":"código incorreto!!!"}
                    )


@app.get('/home')
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )

