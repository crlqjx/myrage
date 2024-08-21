import requests
import psutil

from src.myrage.myrage import Myrage



def test_myrage():

    is_tor = False
    for proc in psutil.process_iter():
        if proc.name() == "tor":
            is_tor = True
    assert is_tor is False

    myrage = Myrage()

    for proc in psutil.process_iter():
        if proc.name() == "tor":
            is_tor = True

    assert is_tor is True

    current_ip_info = requests.get(r"http://ip-api.com/json").json()
    myrage()

    assert current_ip_info['query'] != myrage.ip_info['query']

