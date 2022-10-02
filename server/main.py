from typing import Any
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import reapy


templates = Jinja2Templates(directory="server/templates")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def jsonifyItem(item: reapy.core.Item):
    """
    """
    return {
        "track_name": item.track.name,
        "track_color": item.track.color,
        "start_time": item.position,
        "end_time": item.position + item.length,
    }

def convertSelectedItems(selected_items: list[Any]):
    """
    """
    rv: list[Any] = list()

    for item in selected_items:
        rv.append(jsonifyItem(item))

    return rv

@app.get("/api/reaper/projectinfo")
async def info():
    try:
        CURR_PROJECT = reapy.Project()
    except Exception:
        reapy.tools.reconnect()
        return {
            "error": "No project open."
        }

    return {
        "project_name": CURR_PROJECT.name.replace(".rpp", ""),
        "project_info": {
            "bpm": CURR_PROJECT.bpm,
            "length": CURR_PROJECT.length,
            "time_signature": CURR_PROJECT.time_signature
        },
        "selected_media_items": convertSelectedItems(CURR_PROJECT.selected_items)
    }

@app.post("/api/reaper/control/play")
async def play():
    try:
        CURR_PROJECT = reapy.Project()
    except Exception:
        reapy.tools.reconnect()
        return {
            "error": "No project open."
        }

    CURR_PROJECT.play()


@app.post("/api/reaper/control/pause")
async def pause():
    try:
        CURR_PROJECT = reapy.Project()
    except Exception:
        reapy.tools.reconnect()
        return {
            "error": "No project open."
        }

    CURR_PROJECT.pause()

@app.post("/api/reaper/control/stop")
async def stop():
    try:
        CURR_PROJECT = reapy.Project()
    except Exception:
        reapy.tools.reconnect()
        return {
            "error": "No project open."
        }

    CURR_PROJECT.stop()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
