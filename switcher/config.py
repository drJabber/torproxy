import argparse
import yaml
import os

class _Config:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as y:
            self.config = yaml.safe_load(y)
        parser = argparse.ArgumentParser(description = 'ip switcher config')
        parser.add_argument('--reuse_treshold',help='IPs to use before reusing the current one')
        parser.add_argument('--local_http_proxy',help='local proxy IP and port')
        parser.add_argument('--tor_password',help='Tor password')
        parser.add_argument('--tor_address',help='IP address or resolvable hostname of the Tor controller')
        parser.add_argument('--tor_port',help='port number of the Tor controller')
        parser.add_argument('--new_ip_requests_limit',help='get new IP attempts limit')
        parser.add_argument('--new_ip_requests_period',help='how long to wait after requesting a new IP')
        parser.add_argument('--public_ip_service',help='service to get external ip in text format')
        self.args = parser.parse_args()

    def __getattr__(self, name):
        try:
            return self.config[name]
        except KeyError:
            return getattr(self.args, name)

config=_Config()