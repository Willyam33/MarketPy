import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for doing golive 

def test_post_new_model_golive_valid_dataset_no_scoring():

    # Nominal Test Case 
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 200, valid dataset, no scoring

    endpoint="/new_model_golive"
    r = requests.post(url=url_root+endpoint,
                      headers={"username": "admin",
                              "password": "admin"}) 


    assert (r.text=='"Pas de modèle évalué pour le dernier dataset valide !"')
    assert (r.status_code==200)
