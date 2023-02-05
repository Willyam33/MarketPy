import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting informations for golive decisions 

###############################################################################################################
# API Test for getting golive decision informations - last valid dataset, no scoring, production model exists #
###############################################################################################################

def test_get_golive_decision_informations():

    # Nominal Test Case 
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 200, last valid dataset, no scoring, production model exists

    endpoint="/golive_decision_informations"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 

    retour = json.loads(r.text)
    assert (retour['dataset']['id']==5)
    assert (retour['dataset']['name']=='valid5.csv')
    assert (retour['scorings']['scoring_warning']=='Pas de modèle évalué pour le dernier dataset valide !')
    assert (retour['production_model']['id']==1)
    assert(type(retour['production_model']['date'])==str)
    assert(retour['production_model']['name']=='LinearRegression')
    assert(retour['production_model']['version']=='V1.0')
    assert(type(retour['production_model']['scores'])==str)
    assert(retour['production_model']['dataset_scoring_ids']=="2,4")
    assert(retour['production_model']['remove_date']==None)

    assert (r.status_code==200)
