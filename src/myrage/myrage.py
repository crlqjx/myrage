import psutil
import time
import os

from stem.process import launch_tor_with_config
from stem.control import Controller
from stem import Signal

from requests import Session
from requests.adapters import Retry, HTTPAdapter


from src.myrage import logger


class Myrage:
    request_counter = 0

    def __init__(self):
        self._check_existing_tor_processes()
        self._tor_process = launch_tor_with_config(
            config={
                "ControlPort": os.environ["CONTROL_PORT"],
                "SocksPort": os.environ["SOCKS_PORT"],
                "GeoIPFile": os.environ["GEO_IP_FILE"],
                "GeoIPv6File": os.environ["GEO_IP_V6_FILE"],
                "ExitNodes": os.environ["EXIT_NODES"],
                "StrictNodes": os.environ["STRICT_NODES"],
            },
            tor_cmd=os.environ["TOR_CMD_PATH"],
        )
        self._controller = Controller.from_port(port=int(os.environ["CONTROL_PORT"]))
        self._controller.authenticate()
        self._session = Session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
            "(HTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }
        self._session.mount('http://', adapter=HTTPAdapter(max_retries=Retry(total=10, backoff_factor=2)))
        self._session.proxies = {
            'http': 'socks5h://127.0.0.1:9051',
            'https': 'socks5h://127.0.0.1:9051'
        }

        self.ip_info = None


    @property
    def session(self):
        return self._session()

    def _check_existing_tor_processes(self):
        """Check and kill existing tor processes before starting one"""

        for proc in psutil.process_iter():
            try:
                if proc.name() == "tor":
                    # proc.kill()
                    proc.terminate()
                    break
            except psutil.NoSuchProcess as unknown_process_error:
                logger.log.warning(unknown_process_error)

    def __call__(self):
        """Renewing IP on call"""

        logger.log.info("Renewing tor IP")
        self._controller.signal(Signal.NEWNYM)
        time.sleep(0.5)
        r = self._session.get(r"http://ip-api.com/json")
        self.ip_info = r.json()
        logger.log.info(f"proxy info: {self.ip_info}")

    def __exit__(self):
        for proc in psutil.process_iter():
            if proc.name() == 'tor':
                proc.terminate()


