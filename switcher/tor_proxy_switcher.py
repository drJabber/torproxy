from .config import config
import switcher
import server

def main():
    sw=switcher.Switcher(config)
    srv=server.Server(sw)
    srv.run(config.server_host, config.server_port)