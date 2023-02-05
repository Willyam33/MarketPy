import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting informations for golive decisions 

###########################################################################
# API Test for getting golive decision informations - Failed Access Tests #
###########################################################################

def test_post_new_model_golive_not_admin():

    # Error Test Case : User doing demand is not admin
    # header : username="user1", password="pass1"
    # parameters None
    # return HTTPCode 401,"L'utilisateur n'est pas administrateur !"
    
    endpoint="/new_model_golive"
    r = requests.post(url=url_root+endpoint,
                     headers={"username": "user1",
                              "password": "pass1"}) 

    assert ((json.loads(r.text))['detail']=='L utilisateur n est pas administrateur !')
    assert (r.status_code==401)

def test_post_new_model_golive_bad_password():

    # Error Test Case : Admin password is wrong
    # header : username="admin", password="admi"
    # parameters None
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    endpoint="/new_model_golive"
    r = requests.post(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admi"}) 

    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)
