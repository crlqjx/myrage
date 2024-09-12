from stem.process import launch_tor_with_config
from stem.control import Controller
from requests import Session

from myrage import (
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



def test_tor_config():

    locale_ip = Session().post('http://ip-api.com/json')
    
    config = {
        "ControlPort": str(CONTROL_PORT),
        "SocksPort": str(SOCKS_PORT),
        "GeoIPFile": GEO_IP_FILE,
        "GeoIPv6File": GEO_IP_V6_FILE,
        "ExitNodes": EXIT_NODES,
        "StrictNodes": str(STRICT_NODES),
    }
    
    tor_cmd = TOR_CMD_PATH
    
    tor = launch_tor_with_config(
        config, tor_cmd, take_ownership=True, init_msg_handler=lambda line: print(line)
    )
    controller = Controller.from_port(port=CONTROL_PORT)
    controller.authenticate()
    
    session = Session()
    
    session.proxies = PROXIES
    session.headers = HEADERS
    
    r = session.post("http://ip-api.com/json")
    
    tor.kill()

    assert locale_ip.json()['query'] != r.json()['query']
    
