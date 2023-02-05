import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting predictions with database corruption

########################################
# API Test for getting all predictions #
########################################

def test_get_all_predictions_with_one_prediction_and_corrupted_users_table():

    # Error Test Case : Database is corrupted (users table name)
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('users')

    endpoint="/predictions"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("users")

def test_get_all_predictions_with_one_prediction_and_corrupted_predictions_table():

    # Error Test Case : Database is corrupted (models table name)
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('predictions')

    endpoint="/predictions"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("predictions")

###############################################
# API Test for getting predictions for a user #
###############################################

def test_get_predictions_for_a_user_with_one_prediction_and_corrupted_users_table():

    # Error Test Case : Database is corrupted (users table name)
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('users')

    endpoint="/predictions"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("users")

def test_get_predictions_for_a_user_with_one_prediction_and_corrupted_predictions_table():

    # Error Test Case : Database is corrupted (models table name)
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('predictions')

    endpoint="/predictions"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("predictions")

#######################################################
# API Test for getting predictions details for a user #
#######################################################

def test_get_predictions_details_for_a_user_with_one_prediction_and_corrupted_users_table():

    # Error Test Case : Database is corrupted (users table name)
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('users')

    endpoint="/predictions_details"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("users")

def test_get_predictions_details_for_a_user_with_one_prediction_and_corrupted_predictions_table():

    # Error Test Case : Database is corrupted (predictions table name)
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('predictions')

    endpoint="/predictions_details"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("predictions")

def test_get_predictions_details_for_a_user_with_one_prediction_and_corrupted_production_models_table():

    # Error Test Case : Database is corrupted (production_models table name)
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('production_models')

    endpoint="/predictions_details"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("production_models")
