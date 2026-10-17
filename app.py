from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
from fuzzywuzzy import process

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
	with open("match.json", "r") as f:
		next_match = json.load(f)
	time = next_match["strTime"]
	date = next_match["dateEvent"]
	home_team = next_match["strHomeTeam"]
	away_team = next_match["strAwayTeam"]
	hcrest = next_match["strHomeTeamBadge"]
	acrest = next_match["strAwayTeamBadge"]

	return templates.TemplateResponse("index.html", {"request":request, "home": home_team, "away":away_team, "date": date, "time": time,  "hcrest": hcrest, "acrest": acrest})

@app.get("/standings", response_class=HTMLResponse)
def standings(request: Request):
	with open("standings.json", "r") as f:
		data = json.load(f)
	standings = data['standings'][0]['table']
	return templates.TemplateResponse("standings.html", {"request": request, "standings": standings})

@app.get("/next", response_class=HTMLResponse)
def preview(request: Request):
	with open("data.json", "r") as f:
		next_match = json.load(f)

	fixture_list = next_match["fixture_list"]

	return templates.TemplateResponse("next.html", {"request": request, "fixtures": fixture_list})	
