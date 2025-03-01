from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    return con

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/movies', response_class=HTMLResponse)
def movies(request: Request):
    return templates.TemplateResponse('kino.html', {'request': request})

@app.get("/childrens", response_class=HTMLResponse)
def child(request: Request):
    return templates.TemplateResponse('child.html', {'request': request})

@app.get('/theatre', response_class=HTMLResponse)
def theatre(request: Request):
    return templates.TemplateResponse('theathre.html', {'request': request})

@app.get("/meetings", response_class=HTMLResponse)
def meeting(request: Request):
    return templates.TemplateResponse('shodki.html', {'request': request})

@app.get('/concerts', response_class=HTMLResponse)
def koncert(request: Request):
    return templates.TemplateResponse('koncert.html', {'request': request})




# @app.get("/card/{item_id}", response_class=HTMLResponse)
# def read_item(request: Request, item_id: int):
#     con = get_db()
#     cur = con.cursor()

#     cur.execute('SELECT * FROM items WHERE id = ?', (item_id,))
#     item = cur.fetchone()
#     con.close()

#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return templates.TemplateResponse('card.html', {'request': request, 'item': item})
    