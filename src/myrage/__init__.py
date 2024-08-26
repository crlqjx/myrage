import os

from decolog.logger import Logger


APP_NAME = 'MYRAGE'
LOG_PATH = '/var/log/myrage'

TOR_CMD_PATH = "/usr/sbin/tor"
CONTROL_PORT = 9050
SOCKS_PORT = 9051
GEO_IP_FILE = "/mnt/c/Users/quijo/Desktop/Tor Browser/Browser/TorBrowser/Data/Tor/geoip"
GEO_IP_V6_FILE = "/mnt/c/Users/quijo/Desktop/Tor Browser/Browser/TorBrowser/Data/Tor/geoip6"
EXIT_NODES = "{BE}, {DE}, {IT}"
STRICT_NODES = 1


logger = Logger(
    app_name = os.environ.get('APP_NAME') or APP_NAME,
    dir_path = LOG_PATH
)

