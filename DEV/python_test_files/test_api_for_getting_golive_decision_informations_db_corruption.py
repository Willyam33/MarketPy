import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting informations for golive decisions 

##########################################################################
# API Test for getting golive decision informations - Corrupted database #
##########################################################################

def test_get_golive_decision_informations_corrupted_table_datasets():

    # Error Test Case - Corrupted Table Datasets
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 500, "Erreur d accès à la base de données"

    alter_table("datasets")

    endpoint="/golive_decision_informations"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 


    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("datasets")

def test_get_golive_decision_informations_corrupted_table_production_models():

    # Error Test Case - Corrupted Table production_models
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 500, "Erreur d accès à la base de données"

    alter_table("production_models")

    endpoint="/golive_decision_informations"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 


    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("production_models")

def test_get_golive_decision_informations_corrupted_table_scoring():

    # Error Test Case - Corrupted Table Scoring
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 500, "Erreur d accès à la base de données"

    alter_table("scoring")

    endpoint="/golive_decision_informations"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 


    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("scoring")

