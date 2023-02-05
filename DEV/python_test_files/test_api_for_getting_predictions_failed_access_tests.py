import pytest
import requests
import json
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting predictions - Failed Access Tests

########################################
# API Test for getting all predictions #
########################################

def test_get_all_predictions_not_admin():

    # Error Test Case : User doing demand is not admin (DB UP again)
    # header : username="user1", password="pass1"
    # parameters None
    # return HTTPCode 401,"L'utilisateur n'est pas administrateur !"
    
    endpoint="/predictions"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "user1",
                              "password": "pass1"}) 

    assert ((json.loads(r.text))['detail']=='L utilisateur n est pas administrateur !')
    assert (r.status_code==401)

def test_get_all_predictions_bad_password():

    # Error Test Case : Admin password is wrong
    # header : username="admin", password="admi"
    # parameters None
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    endpoint="/predictions"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admi"}) 

    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)

###############################################
# API Test for getting predictions for a user #
###############################################

def test_get_predictions_for_a_user_not_admin():

    # Error Test Case : User doing demand is not admin (DB UP again)
    # header : username="user1", password="pass1"
    # parameters "user2"
    # return HTTPCode 401,"L'utilisateur n'est pas administrateur !"
    
    endpoint="/predictions"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "user1",
                              "password": "pass1"}) 

    assert ((json.loads(r.text))['detail']=='L utilisateur n est pas administrateur !')
    assert (r.status_code==401)

def test_get_predictions_for_a_user_bad_password():

    # Error Test Case : Admin password is wrong
    # header : username="admin", password="admi"
    # parameters "user2"
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    endpoint="/predictions"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admi"}) 

    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)
    
############################################################
# API Test for getting predictions for a user with details #
############################################################

def test_get_predictions_details_for_a_user_not_admin():

    # Error Test Case : User doing demand is not admin (DB UP again)
    # header : username="user1", password="pass1"
    # parameters "user2"
    # return HTTPCode 401,"L'utilisateur n'est pas administrateur !"
    
    endpoint="/predictions_details"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "user1",
                              "password": "pass1"}) 

    assert ((json.loads(r.text))['detail']=='L utilisateur n est pas administrateur !')
    assert (r.status_code==401)

def test_get_predictions_details_for_a_user_bad_password():

    # Error Test Case : Admin password is wrong
    # header : username="admin", password="admi"
    # parameters "user2"
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    endpoint="/predictions_details"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admi"}) 

    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)
