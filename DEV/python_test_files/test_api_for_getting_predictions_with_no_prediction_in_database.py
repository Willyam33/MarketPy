import pytest
import requests
import json
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting predictions without predictions in database

########################################
# API Test for getting all predictions #
########################################

def test_get_all_predictions_with_no_prediction():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters None
    # return Warning message - No result

    endpoint="/predictions"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"Aucune prédiction n a été trouvée (et probablement aucune n a été effectuée) !"')

###############################################
# API Test for getting predictions for a user #
###############################################

def test_get_predictions_for_a_user_with_no_prediction():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return Warning message - No result

    endpoint="/predictions"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"Aucune prédiction n a été trouvée (et probablement aucune n a été effectuée) pour user2"')

#######################################################
# API Test for getting predictions details for a user #
#######################################################

def test_get_predictions_details_for_a_user_with_no_prediction():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return Warning message - No result

    endpoint="/predictions_details"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"Aucune prédiction n a été trouvée (et probablement aucune n a été effectuée) pour user2"')

