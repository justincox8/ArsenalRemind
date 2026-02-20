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
	with open("data.json", "r") as f:
		next_match = json.load(f)

	time = next_match["time"]
	date = next_match["date"]
	homet = next_match["teams"]["home"]["name"]
	awayt = next_match["teams"]["away"]["name"]
	
	standings_lookup = {}
	for team_entry in next_match["standings"]["standings"][0]["table"]:
		team_name = team_entry["team"]["name"]  # <- must get ["name"]	
		crest_url = team_entry["team"]["crest"]
		standings_lookup[team_name] = crest_url

	team_names_list = list(standings_lookup.keys())

	hmatch_result = process.extractOne(homet, team_names_list)
	if hmatch_result:
		hmatch, hscore = hmatch_result # type: ignore
		hcrest = standings_lookup[hmatch] if hscore > 80 else None
	else:
		hcrest = None

	amatch_result = process.extractOne(awayt, team_names_list)
	if amatch_result:
		amatch, ascore = amatch_result # type: ignore
		acrest = standings_lookup[amatch] if ascore > 80 else None
	else:
		acrest = None

	return templates.TemplateResponse("index.html", {"request":request, "home": homet, "away":awayt, "date": date, "time": time,  "hcrest": hcrest, "acrest": acrest})

@app.get("/standings", response_class=HTMLResponse)
def standings(request: Request):
	with open("data.json", "r") as f:
		data = json.load(f)
	standings = data["standings"]["standings"][0]['table']
	return templates.TemplateResponse("standings.html", {"request": request, "standings": standings})

@app.get("/next", response_class=HTMLResponse)
def preview(request: Request):
	with open("data.json", "r") as f:
		next_match = json.load(f)

	fixture_list = next_match["fixture_list"]

	return templates.TemplateResponse("next.html", {"request": request, "fixtures": fixture_list})	