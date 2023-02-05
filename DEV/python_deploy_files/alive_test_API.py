import os
import sys
import pytest
import requests
import json
import deploy_properties

# Alive test of API

# API URL
url_root = 'http://127.0.0.1:'+deploy_properties.port_API_uvicorn

def test_API_UP():
    
    # Normal Test Case
    # no header 
    # no parameters 
    # return HTTPCode 200,"API UP..."

    endpoint="/"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"API UP..."')

