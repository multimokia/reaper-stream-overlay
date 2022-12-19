import asyncio
import socketio
import eventlet
from eventlet import wsgi
from typing import Any, Callable
import reapy

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

CURR_PROJECT = reapy.Project()
OBSERVERS: dict[int, "ObservableFunctionResult"] = dict()

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

        sio.sleep(0.5)

def fetchProjectName() -> str:
    """
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
    """
    if newVal is None:
        return

    sio.emit("project-name-change", newVal)

def fetchSelectedItems() -> str:
    """
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
    """
    sio.emit("project-selection-change", newVal)

def loopThread():
    # Prep loop
    loop = asyncio.new_event_loop()
    task = loop.create_task(checkObservables())
    loop.run_until_complete(task)

@sio.event
def connect(sid, environ):
    sio.emit("project-name-change", CURR_PROJECT.name.replace(".rpp", ""))
    return

def main():
    # Init handlers
    ObservableFunctionResult(fetchProjectName).subscribe(emitProjectName)
    ObservableFunctionResult(fetchSelectedItems).subscribe(emitSelectedItems)

    eventlet.monkey_patch()
    sio.start_background_task(target=loopThread)
    wsgi.server(eventlet.listen(("", 5000)), app)

    return

if __name__ == "__main__":
    main()
