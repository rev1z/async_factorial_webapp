import signal
import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web
from subproc import start_sub, connect_read_pipe

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    ws = web.WebSocketResponse()
    ws_is_ready = ws.can_prepare(request)
    if not ws_is_ready.ok:
        return aiohttp_jinja2.render_template('index.html', request, {})

    await ws.prepare(request)
    print('client joined')
    await ws.send_json({'action': 'connect'})

    request.app['websockets'].append(ws)
    try:
        while True:
            msg = await ws.receive()
            if msg.type == aiohttp.WSMsgType.text:
                for ws in request.app['websockets']:
                    reader, _= await connect_read_pipe(request.app["factorial"].stdout)
                    item = await reader.readline()
                    await ws.send_json({"action": "sent", "text": item.decode()})
            else:
                break
        print('client disconected')

    finally:
        request.app["websockets"].remove(ws)
    return ws


async def shutdown(app):
    print("close factorial subprocess")
    await app.loop.run_in_executor(None, app['factorial'].send_signal, signal.SIGTERM)
    await app.loop.run_in_executor(None, app['factorial'].wait)
    for ws in app["websockets"]:
        print("closing sockets")
        await ws.close(code=999, message="server shutdown")


async def init():

    app = web.Application()
    app["websockets"] = []
    app.on_shutdown.append(shutdown)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"))
    proc = await start_sub(app.loop)
    app["factorial"] = proc
    app.add_routes(routes)
    return app


web.run_app(init())
