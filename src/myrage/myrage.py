import psutil
import time

from stem.process import launch_tor_with_config
from stem.control import Controller
from stem import Signal

from requests import Session
from requests.adapters import Retry, HTTPAdapter


from myrage import (
    logger,
    CONTROL_PORT,
    SOCKS_PORT,
    GEO_IP_FILE,
    GEO_IP_V6_FILE,
    EXIT_NODES,
    STRICT_NODES,
    TOR_CMD_PATH,

    PROXIES,

    HEADERS
)

class Myrage:
    request_counter = 0

    def __init__(
        self,
        control_port: int = CONTROL_PORT,
        socks_port: int = SOCKS_PORT,
        geo_ip_file: str = GEO_IP_FILE,
        geo_ip_v6_file: str = GEO_IP_V6_FILE,
        exit_nodes: str = EXIT_NODES,
        strict_nodes: int = STRICT_NODES,
        tor_cmd_path: str = TOR_CMD_PATH,
        use_tor: bool = True,
    ):
        self._session = Session()
        self._session.headers = HEADERS
        self._session.mount(
            "http://",
            adapter=HTTPAdapter(max_retries=Retry(total=10, backoff_factor=2)),
        )

        if use_tor is True:
            self.__configure_tor_session(
                control_port=control_port,
                socks_port=socks_port,
                exit_nodes=exit_nodes,
                geo_ip_file=geo_ip_file,
                geo_ip_v6_file=geo_ip_v6_file,
                strict_nodes=strict_nodes,
                tor_cmd_path=tor_cmd_path,
            )

    @property
    def session(self):
        return self._session

    def __configure_tor_session(
        self,
        control_port: int = CONTROL_PORT,
        socks_port: int = SOCKS_PORT,
        geo_ip_file: str = GEO_IP_FILE,
        geo_ip_v6_file: str = GEO_IP_V6_FILE,
        exit_nodes: str = EXIT_NODES,
        strict_nodes: int = STRICT_NODES,
        tor_cmd_path: str = TOR_CMD_PATH,
    ):
        self._check_existing_tor_processes()
        self._tor_process = launch_tor_with_config(
            config={
                "ControlPort": str(control_port),
                "SocksPort": str(socks_port),
                "GeoIPFile": geo_ip_file,
                "GeoIPv6File": geo_ip_v6_file,
                "ExitNodes": exit_nodes,
                "StrictNodes": str(strict_nodes),
            },
            tor_cmd=tor_cmd_path,
            init_msg_handler = lambda line:logger.log.info(line)
        )
        self._controller = Controller.from_port(port=control_port)
        self._controller.authenticate()

        self._session.proxies = PROXIES

    def get_locale_ip_info(self):
        """Store locale ip information"""
        r = Session().get("http://ip-api.com/json")
        return r.json()

    def get_ip_info(self):
        """Store information about the IP that will be used in the session"""
        r = self.session.get("http://ip-api.com/json")
        return r.json()


    def _check_existing_tor_processes(self):
        """Check and kill existing tor processes before starting one"""

        for proc in psutil.process_iter():
            try:
                if proc.name() == "tor":
                    # proc.kill()
                    logger.log.warning(
                        "Trying to terminate an already existing Tor process:"
                        f" process id: {proc.pid} - "
                        f"process name: {proc.name} - "
                        f"user: {proc.username()}"
                    )
                    proc.terminate()
                    break
            except psutil.NoSuchProcess as unknown_process_error:
                logger.log.warning(unknown_process_error)

    def __call__(self):
        """Renewing IP on call"""

        logger.log.info("Renewing tor IP")
        self._controller.signal(Signal.NEWNYM)
        time.sleep(1)
        r = self._session.get(r"http://ip-api.com/json")
        self.ip_info = r.json()
        logger.log.info(f"proxy info: {self.ip_info}")

    def stop(self, kill: bool = False):
        for proc in psutil.process_iter():
            if proc.name() == "tor":
                proc.terminate() if kill is False else proc.kill()

    def __del__(self):
        logger.log.info("Deleting myrage controller and tor instances")
        self._controller.close()
        self._tor_process.kill()
