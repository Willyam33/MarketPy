import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties
import database_functions

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for realizing predictions

def test_predict_ok():
    
    # Normal Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format
    # return - The prediction (float value)

    input = {
        "rating": "4.50",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi" : "0",
        "nb_equip" : "20"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert (r.status_code==200)
    value=float(r.text)
    assert(type(value)==float)
    assert(value>0)

    status, predictions_results=database_functions.get_all_predictions()
    dict_predictions_results = []
    for dict_predictions_row in predictions_results.mappings():
        dict_predictions_results.append(dict_predictions_row)

    assert(status=='OK')
    assert(len(dict_predictions_results)==1)
    assert(dict_predictions_results[0]['id']==1)
    assert(type(dict_predictions_results[0]['date'])==str)
    assert(dict_predictions_results[0]['model_id']==1)
    assert(dict_predictions_results[0]['user_id']==3)
    assert(dict_predictions_results[0]['rating']==4.5)
    assert(dict_predictions_results[0]['tag']=="")
    assert(dict_predictions_results[0]['bedroom']==3)
    assert(dict_predictions_results[0]['bathroom']==1)
    assert(dict_predictions_results[0]['pool']==0)
    assert(dict_predictions_results[0]['jacuzzi']==0)
    assert(dict_predictions_results[0]['nb_equip']==20)
    assert(type(dict_predictions_results[0]['result'])==float)

#test_predict_ok()

def test_predict_one_element_lack():
    
    # Error Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format - minus one information
    # return - The prediction (float value)

    input = {
        "rating": "4.50",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi" : "0"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert (r.status_code==422)

def test_predict_wrong_type_for_parameter():
    
    # Error Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format - minus one information
    # return - The prediction (float value)

    input = {
        "rating": "toto",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi": "0",
        "nb_equip": "20" 
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert (r.status_code==422)

def test_predict_user_unknown():
    
    # Error Test Case
    # header : username="user3", password="pass3"
    # body parameters - Input format
    # return - 401 - "user3 n existe pas"

    input = {
        "rating": "4.5",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi": "0",
        "nb_equip": "20" 
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user3",
                               "password": "pass3"}) 
    assert ((json.loads(r.text))['detail']=='L utilisateur n existe pas !')
    assert (r.status_code==401)

def test_predict_bad_password():
    
    # Error Test Case
    # header : username="user2", password="pass_incorrect"
    # body parameters - Input format
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    input = {
        "rating": "4.5",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi": "0",
        "nb_equip": "20" 
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass_incorrect"}) 
    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)
 
def test_predict_corrupted_production_models_table():
    
    # Error Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format
    # return HTTPCode 500,"Erreur d accès à la base de données"

    alter_table('production_models')

    input = {
        "rating": "4.50",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi" : "0",
        "nb_equip" : "20"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table('production_models')

def test_predict_corrupted_predictions_table():
    
    # Warning Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format
    # return prediction in spite of corruption table

    alter_table('predictions')

    input = {
        "rating": "4.50",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi" : "0",
        "nb_equip" : "20"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert (r.status_code==200)
    value=float(r.text)
    assert(type(value)==float)
    assert(value>0)

    un_alter_table('predictions')

# TODO : Tests on data limit values