
# server_simple.py
from aiohttp import web

class Server:
    def __init__(self,switcher):
        self._switcher=switcher

        self._app = web.Application()
        self._app.add_routes([web.get("/switch", self._handle)])


    async def _make_response(self):
        new_ip=''
        error=''
        state=200
        try:
            new_ip=await self._switcher.get_new_ip()
        except Exception as ex:
            error=f"{ex.__class__}: {str(ex)}"
            state=500
        
        return web.json_response({'ip':new_ip, 'error':error}, status=state)


    async def _handle(self,request):
        return await self._make_response()


    def run(self, host='127.0.0.1', port=80):
        web.run_app(self._app, host=host, port=port)


    async def get_app(self):
        return self._app


