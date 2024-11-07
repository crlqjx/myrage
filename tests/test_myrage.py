import requests
import psutil

from requests import Session

from unittest.mock import patch

from myrage.myrage import Myrage


def test_myrage():


    myrage = Myrage()
    myrage.max_requests = 2

    assert isinstance(myrage, Session)

    assert myrage.request_counter == 0

    current_ip_info = requests.get(r"http://ip-api.com/json").json() # locale ip
    
    assert isinstance(myrage(), Myrage)

    for proc in psutil.process_iter():
        if proc.name() == "tor":
            is_tor = True

    assert is_tor is True

    assert current_ip_info['query'] != myrage.ip_info['query']
    assert current_ip_info['query'] == myrage.get_locale_ip_info()['query']

    myrage.stop()

def test_ip_rotation():

    myrage = Myrage()
   
    with patch.object(myrage, 'renew_ip') as mock_method:
        myrage.max_requests = 2
        for _ in range(3):
            myrage.get(r"http://ip-api.com/json")

        mock_method.assert_called_once()



