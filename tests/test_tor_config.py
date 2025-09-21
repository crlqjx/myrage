import os

from stem.process import launch_tor_with_config
from stem.control import Controller
from requests import Session

from myrage import (
    CONTROL_PORT,
    SOCKS_PORT,
    EXIT_NODES,
    STRICT_NODES,

    PROXIES,
    HEADERS
    
)



def test_tor_config():

    locale_ip = Session().post('http://ip-api.com/json')

    config = {
        "ControlPort": str(CONTROL_PORT),
        "SocksPort": str(SOCKS_PORT),
        "GeoIPFile": os.path.abspath("./src/myrage/geoip"),
        "GeoIPv6File": os.path.abspath("./src/myrage/geoip6"),
        "ExitNodes": EXIT_NODES,
        "StrictNodes": str(STRICT_NODES),
    }
    
    tor = launch_tor_with_config(
        config, 'tor', take_ownership=True, init_msg_handler=lambda line: print(line)
    )

    controller = Controller.from_port(port=CONTROL_PORT)
    controller.authenticate()
    
    session = Session()
    
    session.proxies = PROXIES
    session.headers = HEADERS
    
    r = session.post("http://ip-api.com/json")
    
    tor.kill()

    assert locale_ip.json()['query'] != r.json()['query']
    
