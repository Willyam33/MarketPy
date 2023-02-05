import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting informations for golive decisions 

#############################################################################################
# API Test for getting golive decision informations - no valid dataset, no production model #
#############################################################################################

def test_get_golive_decision_informations():

    # Nominal Test Case 
    # header : username="admin", password="admin"
    # parameters None
    # return HTTPCode 200, no valid dataset, no production model

    endpoint="/golive_decision_informations"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 

    retour = json.loads(r.text)

    assert (retour['dataset']['dataset_warning']=="Aucun dataset n est valide !")
    assert (retour['production_model']['production_model_warning']=='Pas de modele disponible en production !')

    assert (r.status_code==200)
