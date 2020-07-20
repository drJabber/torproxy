from config import config
import switcher
import server

if __name__=='__main__':
    sw=switcher.Switcher(config)
    srv=server.Server(sw)
    srv.run(config.server_host, config.server_port)