from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import arsenal
import json

#initialize app and mount the css files
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

#initialize jinja
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
	with open("next_match.json", "r") as f:
		next_match = json.load(f)
	homet = next_match["teams"]["home"]["name"]
	awayt = next_match["teams"]["away"]["name"]
	return templates.TemplateResponse("index.html", {"request":request, "home": homet, "away":awayt})
