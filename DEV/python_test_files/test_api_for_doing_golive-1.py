import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties
import database_functions

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for doing golive 

def test_post_new_model_golive_nominal_case():

    # Nominal Test Case 
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 200, first succeeded golive

    endpoint="/new_model_golive"
    r = requests.post(url=url_root+endpoint,
                      headers={"username": "admin",
                              "password": "admin"}) 

    assert (r.text=='"Un nouveau modèle est disponible en production !"')
    assert (r.status_code==200)

    # Checking Database

    status, production_models_results=database_functions.get_all_production_models()
    dict_production_models_results = []
    for dict_production_models_row in production_models_results.mappings():
        dict_production_models_results.append(dict_production_models_row)

    assert(status=='OK')
    assert(len(dict_production_models_results)==1)

    assert(dict_production_models_results[0]['id']==1)
    assert(type(dict_production_models_results[0]['date'])==str)
    assert(dict_production_models_results[0]['version']=='V1.0')
    assert(dict_production_models_results[0]['name']=='LinearRegression')
    assert(type(dict_production_models_results[0]['scores'])==str)
    assert(dict_production_models_results[0]['dataset_scoring_ids']=="2")
    assert(dict_production_models_results[0]['remove_date']==None)



