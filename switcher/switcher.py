import asyncio
import aiohttp
import ipaddress
from .config import config
from stem import Signal
from stem.control import Controller
from time import sleep
import errno


class Switcher:
    def __init__(self):
        self._session=aiohttp.ClientSession()

        self.reuse_threshold=config.reuse_threshold
        self.local_http_proxy=config.local_http_proxy
        self.tor_password=config.tor_password
        self.tor_address=config.tor_address
        self.tor_port=config.tor_port
        self.new_ip_requests_limit=config.new_ip_requests_limit
        self.new_ip_requests_period=config.new_ip_requests_period
        self.public_ip_service=config.public_ip_service

        self.used_ips=[]

    async def close(self):
        await self._session.close()


    @property
    async def real_ip(self):
        """
            get external IP
            :returns str
        """

        if not hasattr(self,'_real_ip'):
            async with self._session.get(self.public_ip_service) as resp:
                self._real_ip=await resp.text()
        
        return self._real_ip.strip()

    @property
    async def current_ip(self):
        """
            get current external IP, obtained from proxy
            :returns str
        """

        async with self._session.get(self.public_ip_service, proxy=self.local_http_proxy) as resp:
            self._current_ip=await resp.text()
        
        return self._current_ip.strip()

    async def get_new_ip(self):
        """
            try get new IP from tor proxy
        """
        cur_attempts=0
        cur_ip=''
        
        await self._manage_ip(await self.current_ip)    

        while True:
            if cur_attempts==self.new_ip_requests_limit:
                raise Exception("Unable to obtain new Tor IP")

            cur_attempts+=1
            
            try:
                cur_ip=await self._request_new_ip()
                good_ip=await self._check_ip(cur_ip)
                if not good_ip:
                    print(f'bad new ip: attempt {cur_attempts}, ip: {cur_ip}')
                    continue
            except Exception as ex:
                sleep(self.new_ip_requests_period)
                print(f'exception: attempt {cur_attempts}, ip: {cur_ip}\n {ex} ')
                continue    

            break


        return cur_ip

    async def _request_new_ip(self):
        """
            change tor ip

            :retruns str
        """
        with Controller.from_port(
            address=self.tor_address,port=self.tor_port
        ) as controller:
            # controller.authenticate(password=self.tor_password)
            controller.authenticate(password=self.tor_password)
            controller.signal(Signal.NEWNYM)
            # controller.close()
            sleep(self.new_ip_requests_period)
            return await self.current_ip


    async def _check_ip(self, ip):
        """
            check IP
            :arg ip: current tor ip
            :type ip: str

            :returns bool
        """
        try:
            ipaddress.ip_address(ip)
        except(ValueError):
            return False
        r_ip=await self.real_ip
        if ip==r_ip:
             return False
        return await self._check_ip_is_safe(ip)

    async def _check_ip_is_safe(self, ip):
        """
            check if this ip is not used earlier
            :arg ip: current tor ip
            :type ip: str

            :returns bool 
        """
        return ip not in self.used_ips

    async def _manage_ip(self, ip):
        """
            register/release tor ip
            :arg ip: current tor ip
            :type ip: str
        """
        if not ip in self.used_ips:
            self.used_ips.append(ip)

        if self.reuse_threshold:
            if len(self.used_ips)>self.reuse_threshold:
                del self.used_ips[0]









        
        