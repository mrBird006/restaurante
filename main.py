from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from data.mongo_client import MongoPlateDataClient
import dotenv
import os

dotenv.load_dotenv(override=True)
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

data_client = MongoPlateDataClient(os.getenv('MONGO_CONNECTION_STRING'))  # Use MongoDB client

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    categories = {}
    for plate in data_client.get_all_plates():
        categories.setdefault(plate['category'], []).append(plate)
    return templates.TemplateResponse('index.html', {'request': request, 'categories': categories})


@app.get('/plate/{slug}', response_class=HTMLResponse)
async def plate_detail(request: Request, slug: str):
    plate = data_client.get_plate_by_slug(slug)
    if not plate:
        return HTMLResponse(content='Not Found', status_code=404)
    return templates.TemplateResponse('detail.html', {'request': request, 'plate': plate})


@app.get('/api/plate/{slug}')
async def plate_json(slug: str):
    plate = data_client.get_plate_by_slug(slug)
    if not plate:
        return JSONResponse(status_code=404, content={"error": "Plate not found"})
    return plate


@app.post('/api/plate/{slug}/like')
async def like_plate(slug: str, email: str = Form(...), action: str = Form(...)):
    if not data_client.get_plate_by_slug(slug):
        return JSONResponse(status_code=404, content={"error": "Plate not found"})

    if action == "like":
        data_client.add_like(slug, email)
    elif action == "dislike":
        data_client.add_dislike(slug, email)
    elif action == "none":
        data_client.remove_reaction(slug, email)

    plate = data_client.get_plate_by_slug(slug)
    return {"likes": len(plate['likes']), "dislikes": len(plate['dislikes'])}


@app.post('/api/plate/{slug}/comment')
async def comment_plate(slug: str, name: str = Form(...), comment: str = Form(...)):
    if not data_client.get_plate_by_slug(slug):
        return JSONResponse(status_code=404, content={"error": "Plate not found"})
    
    data_client.add_comment(slug, name, comment)
    return RedirectResponse(f"/plate/{slug}", status_code=303)
