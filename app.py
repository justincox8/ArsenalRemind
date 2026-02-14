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

	time = next_match["time"]
	date = next_match["date"]
	homet = next_match["teams"]["home"]["name"]
	awayt = next_match["teams"]["away"]["name"]
	fixture_list = next_match["fixture_list"]
	return templates.TemplateResponse("index.html", {"request":request, "home": homet, "away":awayt, "date": date, "time": time, "fixtures": fixture_list})

@app.get("/standings", response_class=HTMLResponse)
def standings(request: Request):
	with open("next_match.json", "r") as f:
		data = json.load(f)
	standings = data["standings"]["standings"][0]['table']
	return templates.TemplateResponse("standings.html", {"request": request, "standings": standings})