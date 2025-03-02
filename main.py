from fastapi import FastAPI, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
from init_db import init_db
from starlette.middleware.sessions import SessionMiddleware
from functools import wraps

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")  # Замените на свой секретный ключ
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Захардкоженные учетные данные (в реальном проекте следует использовать безопасное хранение)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def check_auth(request: Request):
    is_authenticated = request.session.get("authenticated", False)
    if not is_authenticated:
        raise HTTPException(status_code=303, detail="Unauthorized", headers={"Location": "/login"})
    return True

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["authenticated"] = True
        return RedirectResponse(url="/admin", status_code=303)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Неверное имя пользователя или пароль"}
    )

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

init_db()

def get_db():
    con = sqlite3.connect('base.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con


@app.get("/all-items", response_class=HTMLResponse)
def get_all_items(request: Request):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM items')
        items = cur.fetchall()
        return templates.TemplateResponse('items.html', {
            'request': request,
            'items': items
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()




@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('''
            SELECT id, title, description, url_image, 'movies' as source 
            FROM movies
            UNION ALL
            SELECT id, title, description, url_image, 'concerts' as source 
            FROM concerts
            UNION ALL
            SELECT id, title, description, url_image, 'theatre' as source 
            FROM theatre
            UNION ALL
            SELECT id, title, description, url_image, 'childrens' as source 
            FROM childrens
            UNION ALL
            SELECT id, title, description, url_image, 'meetings' as source 
            FROM meetings
            ORDER BY id DESC
            LIMIT 5
        ''')
        latest_items = cur.fetchall()
        print(f"Found {len(latest_items) if latest_items else 0} items")  # Debug print
        
        # Для отладки выведем содержимое первого элемента, если он есть
        if latest_items and len(latest_items) > 0:
            print(f"First item: {dict(latest_items[0])}")
        
        # Получаем последние 5 записей из каждой таблицы для секций
        cur.execute('SELECT * FROM movies ORDER BY id DESC LIMIT 5')
        movies = cur.fetchall()
        
        cur.execute('SELECT * FROM concerts ORDER BY id DESC LIMIT 5')
        concerts = cur.fetchall()
        
        cur.execute('SELECT * FROM theatre ORDER BY id DESC LIMIT 5')
        theatre = cur.fetchall()
        
        cur.execute('SELECT * FROM childrens ORDER BY id DESC LIMIT 5')
        childrens = cur.fetchall()
        
        cur.execute('SELECT * FROM meetings ORDER BY id DESC LIMIT 5')
        meetings = cur.fetchall()
        
        return templates.TemplateResponse('index.html', {
            'request': request,
            'active_page': 'index',
            'latest_items': latest_items if latest_items else [],
            'movies': movies,
            'concerts': concerts,
            'theatre': theatre,
            'childrens': childrens,
            'meetings': meetings
        })
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")  # Debug print
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()


@app.get('/movies', response_class=HTMLResponse)
def movies(request: Request):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM movies')
        items = cur.fetchall()
        return templates.TemplateResponse('kino.html', {
            'request': request,
            'items': items
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()


@app.get("/childrens", response_class=HTMLResponse)
def child(request: Request):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM childrens')
        items = cur.fetchall()
        return templates.TemplateResponse('child.html', {
            'request': request,
            'items': items
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.get('/theatre', response_class=HTMLResponse)
def theatre(request: Request):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM theatre')
        items = cur.fetchall()
        return templates.TemplateResponse('theathre.html', {
            'request': request,
            'items': items
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.get("/meetings", response_class=HTMLResponse)
def meeting(request: Request):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM meetings')
        items = cur.fetchall()
        return templates.TemplateResponse('shodki.html', {
            'request': request,
            'items': items
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.get('/concerts', response_class=HTMLResponse, name="concerts")
def concert(request: Request):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM concerts')
        items = cur.fetchall()
        return templates.TemplateResponse('koncert.html', {
            'request': request,
            'items': items
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()


@app.get("/additems", response_class=HTMLResponse)
async def show_form(request: Request, authenticated: bool = Depends(check_auth)):
    return templates.TemplateResponse('addfilms.html', {'request': request})



@app.post("/additems", response_class=HTMLResponse)
async def additems(
    request: Request,
    authenticated: bool = Depends(check_auth),
    category: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    link: str = Form(...),
    commentary: str = Form(None),
    rating: str = Form(None),
    age_restriction: str = Form(...)
):
    con = get_db()
    cur = con.cursor()
    message = ""
    
    try:
        if not title.strip():
            raise ValueError("Название не может быть пустым")
        if not description.strip():
            raise ValueError("Описание не может быть пустым")
        if not link.strip():
            raise ValueError("Ссылка на обложку не может быть пустой")
            
        valid_categories = ['Фильм', 'Детям', 'Концерты', 'Встречи', 'Театр']
        if category not in valid_categories:
            raise ValueError("Неверная категория")

        if category == 'Фильм':
            cur.execute('INSERT INTO movies (title, description, url_image, commentary, rating, age_restriction) VALUES (?, ?, ?, ?, ?, ?)', 
                       (title, description, link, commentary, rating, age_restriction))
        elif category == 'Детям':
            cur.execute('INSERT INTO childrens (title, description, url_image, commentary, rating, age_restriction) VALUES (?, ?, ?, ?, ?, ?)', 
                       (title, description, link, commentary, rating, age_restriction))
        elif category == 'Концерты':
            cur.execute('INSERT INTO concerts (title, description, url_image, commentary, rating, age_restriction) VALUES (?, ?, ?, ?, ?, ?)', 
                       (title, description, link, commentary, rating, age_restriction))
        elif category == 'Встречи':
            cur.execute('INSERT INTO meetings (title, description, url_image, commentary, rating, age_restriction) VALUES (?, ?, ?, ?, ?, ?)', 
                       (title, description, link, commentary, rating, age_restriction))
        elif category == 'Театр':
            cur.execute('INSERT INTO theatre (title, description, url_image, commentary, rating, age_restriction) VALUES (?, ?, ?, ?, ?, ?)', 
                       (title, description, link, commentary, rating, age_restriction))
        con.commit()
        message = "Элемент успешно добавлен!"
    except ValueError as e:
        message = f"Ошибка валидации: {str(e)}"
    except sqlite3.Error as e:
        message = f"Ошибка базы данных: {str(e)}"
    except Exception as e:
        message = f"Неизвестная ошибка: {str(e)}"
    finally:
        con.close()

    return templates.TemplateResponse('addfilms.html', {
        'request': request,
        'message': message,
    })

@app.post("/delete/{category}/{id}", response_class=HTMLResponse)
def delete_item(request: Request, category: str, id: int):
    con = get_db()
    cur = con.cursor()
    message = ""
    
    try:
        table_name = {
            'movies': 'movies',
            'childrens': 'childrens',
            'concerts': 'concerts',
            'meetings': 'meetings',
            'theatre': 'theatre'
        }.get(category)
        
        if not table_name:
            raise ValueError("Неверная категория")
            
        cur.execute(f'DELETE FROM {table_name} WHERE id = ?', (id,))
        con.commit()
        message = "Элемент успешно удален!"
        
    except sqlite3.Error as e:
        message = f"Ошибка базы данных: {str(e)}"
    except Exception as e:
        message = f"Неизвестная ошибка: {str(e)}"
    finally:
        con.close()
    
    return RedirectResponse(url="/admin", status_code=303)


@app.get('/movie/{id}', response_class=HTMLResponse)
def cardm(request: Request, id: int):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM movies WHERE id = ?', (id,))
        item = cur.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return templates.TemplateResponse('card.html', {
            'request': request,
            'item': dict(item)
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()


@app.get('/concert/{id}', response_class=HTMLResponse)
def cardc(request: Request, id: int):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM concerts WHERE id = ?', (id,))
        item = cur.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return templates.TemplateResponse('card.html', {
            'request': request,
            'item': dict(item)
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.get('/theatre/{id}', response_class=HTMLResponse)
def cardt(request: Request, id: int):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM theatre WHERE id = ?', (id,))
        item = cur.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return templates.TemplateResponse('card.html', {
            'request': request,
            'item': dict(item)
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.get('/child/{id}', response_class=HTMLResponse)
def cardch(request: Request, id: int):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM childrens WHERE id = ?', (id,))
        item = cur.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return templates.TemplateResponse('card.html', {
            'request': request,
            'item': dict(item)
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.get('/meeting/{id}', response_class=HTMLResponse)
def cardme(request: Request, id: int):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM meetings WHERE id = ?', (id,))
        item = cur.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return templates.TemplateResponse('card.html', {
            'request': request,
            'item': dict(item)
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, authenticated: bool = Depends(check_auth)):
    con = get_db()
    cur = con.cursor()
    all_items = {}
    
    try:
        # Получаем все элементы из каждой таблицы
        cur.execute('SELECT * FROM movies')
        all_items['Фильмы'] = cur.fetchall()
        
        cur.execute('SELECT * FROM concerts')
        all_items['Концерты'] = cur.fetchall()
        
        cur.execute('SELECT * FROM theatre')
        all_items['Театр'] = cur.fetchall()
        
        cur.execute('SELECT * FROM childrens')
        all_items['Детям'] = cur.fetchall()
        
        cur.execute('SELECT * FROM meetings')
        all_items['Встречи'] = cur.fetchall()
        
        return templates.TemplateResponse('admin.html', {
            'request': request,
            'all_items': all_items
        })
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()