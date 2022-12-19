import asyncio
import socketio
import eventlet
from eventlet import wsgi
from typing import Any, Callable
import reapy
from strenum import StrEnum

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

CURR_PROJECT = reapy.Project()
OBSERVERS: dict[int, "ObservableFunctionResult"] = dict()

class SocketServerEvents(StrEnum):
    ProjectNameChange = "project-name-change"
    ItemSelectionChange = "project-selection-change"
    MutedChannelsChange = "project-muted-channels-change"
    SolodChannelsChange = "project-solod-channels-change"


class ObservableFunctionResult:
    def __init__(self, func: Callable[[], Any]) -> "ObservableFunctionResult":
        """
        ObservableFunctionResult constructor

        IN:
            func - The function to watch. Takes no arguments, can return Anything

        OUT:
            The observable function result
        """
        self.id = len(OBSERVERS)
        self.handlers: list[Callable[[Any, Any], None]] = []
        self.callable = func
        self.callable_result = func()

        OBSERVERS[self.id] = self

    def subscribe(self, handler: Callable[[Any, Any], None]) -> None:
        """
        Attaches an onChange handler to this Observable which will be fired
        when checkHandlers is called, assuming a change has occurred

        IN:
            handler - A function that accepts two values as input (old_value, new_value) -> None
        """
        handler(None, self.callable_result)
        self.handlers.append(handler)

    def checkHandlers(self) -> None:
        """
        Checks for a change and calls attached handlers if one is detected
        """
        new_result = self.callable()

        if new_result != self.callable_result:
            for handler in self.handlers:
                print(f"Change detected in handler {self.id}:\n[OLD]: {self.callable_result}\n[NEW]: {new_result}\n\n")
                handler(self.callable_result, new_result)

        self.callable_result = new_result

async def checkObservables() -> None:
    """
    Checks observables and runs their change handlers
    """
    while True:
        for observable in OBSERVERS.values():
            observable.checkHandlers()

        sio.sleep(0.1)

def fetchProjectName() -> str:
    """
    Gets project name
    """
    global CURR_PROJECT
    try:
        CURR_PROJECT = reapy.Project()
        return CURR_PROJECT.name.replace(".rpp", "")

    except Exception:
        reapy.tools.reconnect()
        return "No project open"

def emitProjectName(oldVal, newVal) -> None:
    """
    Emits a websocket event for the project name change/set
    """
    if newVal is None:
        newVal = "No project open."

    sio.emit(SocketServerEvents.ProjectNameChange, newVal)

def fetchSelectedItems() -> str:
    """
    Gets the selected items in the project
    """
    global CURR_PROJECT
    try:
        CURR_PROJECT = reapy.Project()

        if not CURR_PROJECT.selected_items:
            return None

        item = CURR_PROJECT.selected_items[0]

        return {
            "track_name": item.track.name,
            "track_color": item.track.color,
            "start_time": item.position,
            "end_time": item.position + item.length,
        }

    except Exception:
        reapy.tools.reconnect()
        return None

def emitSelectedItems(oldVal, newVal) -> None:
    """
    Emits a websocket event for selection change
    """
    sio.emit(SocketServerEvents.ItemSelectionChange, newVal)

def fetchMutedChannels():
    """
    Fetches all muted channels in the project
    """
    global CURR_PROJECT
    try:
        CURR_PROJECT = reapy.Project()

        if not CURR_PROJECT:
            return []

        return [
            { "track_name": track.name, "track_color": track.color }
            for track in filter(lambda x: x.is_muted, CURR_PROJECT.tracks)
        ]

    except Exception:
        reapy.tools.reconnect()
        return []

def emitMutedChannels(oldVal, newVal) -> None:
    """
    Emits a websocket event for muted channels change
    """
    sio.emit(SocketServerEvents.MutedChannelsChange, newVal)

def fetchSolodChannels():
    """
    Fetches all Solo'd channels in the project
    """
    global CURR_PROJECT
    try:
        CURR_PROJECT = reapy.Project()

        if not CURR_PROJECT:
            return []

        return [
            { "track_name": track.name, "track_color": track.color }
            for track in filter(lambda x: x.is_solo, CURR_PROJECT.tracks)
        ]

    except Exception:
        reapy.tools.reconnect()
        return []

def emitSolodChannels(oldVal, newVal) -> None:
    """
    Emits a websocket event for Solo'd channels change
    """
    sio.emit(SocketServerEvents.SolodChannelsChange, newVal)


### Loop related
def loopThread():
    # Prep loop
    loop = asyncio.new_event_loop()
    task = loop.create_task(checkObservables())
    loop.run_until_complete(task)

@sio.event
def connect(sid, environ):
    sio.emit(SocketServerEvents.ProjectNameChange, CURR_PROJECT.name.replace(".rpp", ""))
    return

def main():
    # Init handlers
    ObservableFunctionResult(fetchProjectName).subscribe(emitProjectName)
    ObservableFunctionResult(fetchSelectedItems).subscribe(emitSelectedItems)
    ObservableFunctionResult(fetchMutedChannels).subscribe(emitMutedChannels)
    ObservableFunctionResult(fetchSolodChannels).subscribe(emitSolodChannels)

    eventlet.monkey_patch()
    sio.start_background_task(target=loopThread)
    wsgi.server(eventlet.listen(("", 5000)), app)

    return

if __name__ == "__main__":
    main()
