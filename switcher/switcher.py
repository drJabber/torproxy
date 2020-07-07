import asyncio
import aiohttp
from config import config



class Switcher:
    def __init__(self):
        self.reuse_threshold=config.reuse_threshold
        self.local_http_proxy=config.local_http_proxy
        self.tor_password=config.tor_password
        self.tor_address=config.tor_address
        self.tor_port=config.tor_port
        self.new_ip_requests_limit=config.new_ip_requests_limit
        self.new_ip_requests_period=config.new_ip_requests_period
        self.public_ip_service=config.public_ip_service

        self.used_ips=[]

        print(self.public_ip_service)


switcher=Switcher()

        
        