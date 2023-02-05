import pytest
import requests
import json
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Test API functions for getting predictions with one prediction in database

########################################
# API Test for getting all predictions #
########################################

def test_get_all_predictions_with_one_prediction():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters None
    # return - One result with prediction features, result anf user_id who did the prediction

    endpoint="/predictions"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert ((json.loads(r.text))[0]['id']==1)
    assert ((json.loads(r.text))[0]['model_id']==1)
    assert ((json.loads(r.text))[0]['user_id']==3)
    assert ((json.loads(r.text))[0]['rating']==4.5)
    assert ((json.loads(r.text))[0]['tag']=='')
    assert ((json.loads(r.text))[0]['bedroom']==3)
    assert ((json.loads(r.text))[0]['bathroom']==1)
    assert ((json.loads(r.text))[0]['pool']==0)
    assert ((json.loads(r.text))[0]['jacuzzi']==0)
    assert ((json.loads(r.text))[0]['nb_equip']==20)
    assert (type((json.loads(r.text))[0]['result'])==float)
    assert (type((json.loads(r.text))[0]['date'])==str)

###############################################
# API Test for getting predictions for a user #
###############################################

def test_get_predictions_for_a_user_with_one_prediction():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return - One result with prediction features and result

    endpoint="/predictions"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert ((json.loads(r.text))[0]['model_id']==1)
    assert ((json.loads(r.text))[0]['rating']==4.5)
    assert ((json.loads(r.text))[0]['tag']=='')
    assert ((json.loads(r.text))[0]['bedroom']==3)
    assert ((json.loads(r.text))[0]['bathroom']==1)
    assert ((json.loads(r.text))[0]['pool']==0)
    assert ((json.loads(r.text))[0]['jacuzzi']==0)
    assert ((json.loads(r.text))[0]['nb_equip']==20)
    assert (type((json.loads(r.text))[0]['result'])==float)
    assert (type((json.loads(r.text))[0]['date'])==str)

#######################################################
# API Test for getting predictions details for a user #
#######################################################

def test_get_predictions_details_for_a_user_with_one_prediction():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return - One result with details on production model used for prediction

    endpoint="/predictions_details"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert ((json.loads(r.text))[0]['predictions.id']==1)
    assert ((json.loads(r.text))[0]['model_id']==1)
    assert ((json.loads(r.text))[0]['version']=='V1.0')
    assert ((json.loads(r.text))[0]['name']=='LinearRegression')
    assert ((json.loads(r.text))[0]['rating']==4.5)
    assert ((json.loads(r.text))[0]['bedroom']==3)
    assert ((json.loads(r.text))[0]['bathroom']==1)
    assert ((json.loads(r.text))[0]['pool']==0)
    assert ((json.loads(r.text))[0]['jacuzzi']==0)
    assert ((json.loads(r.text))[0]['nb_equip']==20)
    assert (type((json.loads(r.text))[0]['result'])==float)
    assert (type((json.loads(r.text))[0]['predictions.date'])==str)
    assert (type((json.loads(r.text))[0]['production_models.date'])==str)

