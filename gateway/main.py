# Gateway entry point (FastAPI + Jinja2)
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/')
def read_root(request):
    return templates.TemplateResponse('base.html', {'request': request})
