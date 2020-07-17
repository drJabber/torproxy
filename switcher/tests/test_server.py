import asyncio
import pytest
import ipaddress
# from aiohttp import pytest_plugun
from ..server import Server
from ..config import config
from ..switcher import Switcher


@pytest.fixture(scope="session")
def loop():
    return asyncio.get_event_loop()


@pytest.fixture
async def switcher():
    return Switcher(config)

@pytest.fixture
async def client(aiohttp_client, switcher):
    server=Server(switcher)
    return await aiohttp_client(await server.get_app())
 

@pytest.mark.asyncio
async def test_change_ip(client,loop):
    resp=await client.get('/switch')
    assert resp.status==200, await resp.text()
    data=await resp.json()
    assert data['error']=='', await resp.text()
    ipaddress.ip_address(data['ip']) 
    


