import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting informations for golive decisions 

#########################################################################################################
# API Test for getting golive decision informations - last valid dataset, scorings, no production model #
#########################################################################################################

def test_get_golive_decision_informations():

    # Nominal Test Case 
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 200, last valid dataset, scorings, no production model

    endpoint="/golive_decision_informations"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 


    retour = json.loads(r.text)

    assert (retour['dataset']['id']==2)
    assert (retour['dataset']['name']=='valid3.csv')

    assert(len(retour['scorings'])==3)
    assert(retour['scorings'][0]['id']==4)
    assert(retour['scorings'][0]['model_library']=='sklearn.linear_model')
    assert(retour['scorings'][0]['model_name']=='LinearRegression')
    assert(type(retour['scorings'][0]['score'])==float)
    assert(retour['scorings'][0]['best_model']==1)
    assert(retour['scorings'][1]['id']==5)
    assert(retour['scorings'][1]['model_library']=='sklearn.tree')
    assert(retour['scorings'][1]['model_name']=='DecisionTreeRegressor')
    assert(type(retour['scorings'][1]['score'])==float)
    assert(retour['scorings'][1]['best_model']==0)
    assert(retour['scorings'][2]['id']==6)
    assert(retour['scorings'][2]['model_library']=='sklearn.ensemble')
    assert(retour['scorings'][2]['model_name']=='RandomForestRegressor')
    assert(type(retour['scorings'][2]['score'])==float)
    assert(retour['scorings'][2]['best_model']==0)

    assert (retour['production_model']['production_model_warning']=='Pas de modele disponible en production !')
    assert (r.status_code==200)
