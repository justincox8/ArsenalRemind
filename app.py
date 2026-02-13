from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import arsenal

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
	data = arsenal.get_matches()
	next_match = arsenal.next_match(data)
	homet = next_match["teams"]["home"]["name"]
	awayt = next_match["teams"]["away"]["name"]
	return templates.TemplateResponse("index.html", {"request":request, "home": homet, "away":awayt})
