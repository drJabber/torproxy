import pytest
from ..switcher import Switcher
from ..config import config

@pytest.mark.asyncio
async def test_switcher_real_ip():
    sw=Switcher(config)
    ip=await sw.real_ip
    await sw.close()
    print(f'\nIP address is {ip}')
    assert (ip!=None)

@pytest.mark.asyncio
async def test_switcher_current_ip():
    sw=Switcher(config)
    ip=await sw.current_ip
    await sw.close()
    print(f'\ncurrent IP address is {ip}')
    assert (ip!=None)    

@pytest.mark.asyncio
async def test_switcher_get_new_ip():
    sw=Switcher(config)
    ip1=await sw.current_ip
    print(f'\ncurrent IP address is {ip1}')
    ip2=await sw.get_new_ip()
    print(f'\nnew IP address is {ip2}')
    await sw.close()
    assert (ip1!=ip2)        