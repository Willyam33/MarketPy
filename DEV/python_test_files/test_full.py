import pytest
import requests
import json
from test_functions import alter_table, un_alter_table, copy_of_csv_file_from_test_folder_to_incoming_folder
import test_properties
import database_functions
import listen_to_dataset_arrival

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

# Tests full / End To End

# Test full 1 : New valid dataset + GO Live
def test_full_1():
    
    # Copy a valid CSV file in Incoming Folder
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid.csv")
    
    listen_to_dataset_arrival.listening_workflow()

    # Go Live

    endpoint="/new_model_golive"
    r = requests.post(url=url_root+endpoint,
                      headers={"username": "admin",
                              "password": "admin"}) 

    # Do Prediction

    input = {
        "rating": "4.60",
        "tag": "",
        "bedroom": "1",
        "bathroom": "4",
        "pool": "1",
        "jacuzzi" : "1",
        "nb_equip" : "15"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user1",
                               "password": "pass1"}) 
    assert (r.status_code==200)
    value=float(r.text)
    assert(type(value)==float)
    assert(value>0)

    status, predictions_results=database_functions.get_all_predictions()
    dict_predictions_results = []
    for dict_predictions_row in predictions_results.mappings():
        dict_predictions_results.append(dict_predictions_row)

    assert(status=='OK')
    assert(len(dict_predictions_results)==2)
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

    assert(dict_predictions_results[1]['id']==2)
    assert(type(dict_predictions_results[1]['date'])==str)
    assert(dict_predictions_results[1]['model_id']==2)
    assert(dict_predictions_results[1]['user_id']==2)
    assert(dict_predictions_results[1]['rating']==4.6)
    assert(dict_predictions_results[1]['tag']=="")
    assert(dict_predictions_results[1]['bedroom']==1)
    assert(dict_predictions_results[1]['bathroom']==4)
    assert(dict_predictions_results[1]['pool']==1)
    assert(dict_predictions_results[1]['jacuzzi']==1)
    assert(dict_predictions_results[1]['nb_equip']==15)
    assert(type(dict_predictions_results[1]['result'])==float)

    # Get Predictions

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

    assert ((json.loads(r.text))[1]['id']==2)
    assert ((json.loads(r.text))[1]['model_id']==2)
    assert ((json.loads(r.text))[1]['user_id']==2)
    assert ((json.loads(r.text))[1]['rating']==4.6)
    assert ((json.loads(r.text))[1]['tag']=='')
    assert ((json.loads(r.text))[1]['bedroom']==1)
    assert ((json.loads(r.text))[1]['bathroom']==4)
    assert ((json.loads(r.text))[1]['pool']==1)
    assert ((json.loads(r.text))[1]['jacuzzi']==1)
    assert ((json.loads(r.text))[1]['nb_equip']==15)
    assert (type((json.loads(r.text))[1]['result'])==float)
    assert (type((json.loads(r.text))[1]['date'])==str)

    endpoint="/predictions_details"
    parameters="/user1"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 

    assert ((json.loads(r.text))[0]['predictions.id']==2)
    assert ((json.loads(r.text))[0]['model_id']==2)
    assert ((json.loads(r.text))[0]['version']=='V1.1')
    assert ((json.loads(r.text))[0]['name']=='LinearRegression')
    assert ((json.loads(r.text))[0]['rating']==4.6)
    assert ((json.loads(r.text))[0]['tag']=='')
    assert ((json.loads(r.text))[0]['bedroom']==1)
    assert ((json.loads(r.text))[0]['bathroom']==4)
    assert ((json.loads(r.text))[0]['pool']==1)
    assert ((json.loads(r.text))[0]['jacuzzi']==1)
    assert ((json.loads(r.text))[0]['nb_equip']==15)
    assert (type((json.loads(r.text))[0]['result'])==float)
    assert (type((json.loads(r.text))[0]['predictions.date'])==str)
    assert (type((json.loads(r.text))[0]['production_models.date'])==str)

# Test full 2 : New model + New valid dataset + GO Live
def test_full_2():
    
    # New model : MLP Regressor : The best ;)
    endpoint="/add_model"
    parameters="/sklearn.neural_network/MLPRegressor"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"MLPRegressor a été ajouté !"')

    # Copy a valid CSV file in Incoming Folder
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid2.csv")
    
    listen_to_dataset_arrival.listening_workflow()

    # Go Live

    endpoint="/new_model_golive"
    r = requests.post(url=url_root+endpoint,
                      headers={"username": "admin",
                              "password": "admin"}) 

    # Do Prediction

    input = {
        "rating": "4.80",
        "tag": "",
        "bedroom": "3",
        "bathroom": "5",
        "pool": "0",
        "jacuzzi" : "1",
        "nb_equip" : "25"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user1",
                               "password": "pass1"}) 
    assert (r.status_code==200)
    value=float(r.text)
    assert(type(value)==float)
    assert(value>0)

    status, predictions_results=database_functions.get_all_predictions()
    dict_predictions_results = []
    for dict_predictions_row in predictions_results.mappings():
        dict_predictions_results.append(dict_predictions_row)

    assert(status=='OK')
    assert(len(dict_predictions_results)==3)
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

    assert(dict_predictions_results[1]['id']==2)
    assert(type(dict_predictions_results[1]['date'])==str)
    assert(dict_predictions_results[1]['model_id']==2)
    assert(dict_predictions_results[1]['user_id']==2)
    assert(dict_predictions_results[1]['rating']==4.6)
    assert(dict_predictions_results[1]['tag']=="")
    assert(dict_predictions_results[1]['bedroom']==1)
    assert(dict_predictions_results[1]['bathroom']==4)
    assert(dict_predictions_results[1]['pool']==1)
    assert(dict_predictions_results[1]['jacuzzi']==1)
    assert(dict_predictions_results[1]['nb_equip']==15)
    assert(type(dict_predictions_results[1]['result'])==float)

    assert(dict_predictions_results[2]['id']==3)
    assert(type(dict_predictions_results[2]['date'])==str)
    assert(dict_predictions_results[2]['model_id']==3)
    assert(dict_predictions_results[2]['user_id']==2)
    assert(dict_predictions_results[2]['rating']==4.8)
    assert(dict_predictions_results[2]['tag']=="")
    assert(dict_predictions_results[2]['bedroom']==3)
    assert(dict_predictions_results[2]['bathroom']==5)
    assert(dict_predictions_results[2]['pool']==0)
    assert(dict_predictions_results[2]['jacuzzi']==1)
    assert(dict_predictions_results[2]['nb_equip']==25)
    assert(type(dict_predictions_results[2]['result'])==float)

    # Get Predictions

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

    assert ((json.loads(r.text))[1]['id']==2)
    assert ((json.loads(r.text))[1]['model_id']==2)
    assert ((json.loads(r.text))[1]['user_id']==2)
    assert ((json.loads(r.text))[1]['rating']==4.6)
    assert ((json.loads(r.text))[1]['tag']=='')
    assert ((json.loads(r.text))[1]['bedroom']==1)
    assert ((json.loads(r.text))[1]['bathroom']==4)
    assert ((json.loads(r.text))[1]['pool']==1)
    assert ((json.loads(r.text))[1]['jacuzzi']==1)
    assert ((json.loads(r.text))[1]['nb_equip']==15)
    assert (type((json.loads(r.text))[1]['result'])==float)
    assert (type((json.loads(r.text))[1]['date'])==str)

    assert ((json.loads(r.text))[2]['id']==3)
    assert ((json.loads(r.text))[2]['model_id']==3)
    assert ((json.loads(r.text))[2]['user_id']==2)
    assert ((json.loads(r.text))[2]['rating']==4.8)
    assert ((json.loads(r.text))[2]['tag']=='')
    assert ((json.loads(r.text))[2]['bedroom']==3)
    assert ((json.loads(r.text))[2]['bathroom']==5)
    assert ((json.loads(r.text))[2]['pool']==0)
    assert ((json.loads(r.text))[2]['jacuzzi']==1)
    assert ((json.loads(r.text))[2]['nb_equip']==25)
    assert (type((json.loads(r.text))[2]['result'])==float)
    assert (type((json.loads(r.text))[2]['date'])==str)

    endpoint="/predictions_details"
    parameters="/user1"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 

    assert ((json.loads(r.text))[0]['predictions.id']==2)
    assert ((json.loads(r.text))[0]['model_id']==2)
    assert ((json.loads(r.text))[0]['version']=='V1.1')
    assert ((json.loads(r.text))[0]['name']=='LinearRegression')
    assert ((json.loads(r.text))[0]['rating']==4.6)
    assert ((json.loads(r.text))[0]['tag']=='')
    assert ((json.loads(r.text))[0]['bedroom']==1)
    assert ((json.loads(r.text))[0]['bathroom']==4)
    assert ((json.loads(r.text))[0]['pool']==1)
    assert ((json.loads(r.text))[0]['jacuzzi']==1)
    assert ((json.loads(r.text))[0]['nb_equip']==15)
    assert (type((json.loads(r.text))[0]['result'])==float)
    assert (type((json.loads(r.text))[0]['predictions.date'])==str)
    assert (type((json.loads(r.text))[0]['production_models.date'])==str)

    assert ((json.loads(r.text))[1]['predictions.id']==3)
    assert ((json.loads(r.text))[1]['model_id']==3)
    assert ((json.loads(r.text))[1]['version']=='V2.0')
    assert ((json.loads(r.text))[1]['name']=='MLPRegressor')
    assert ((json.loads(r.text))[1]['rating']==4.8)
    assert ((json.loads(r.text))[1]['tag']=='')
    assert ((json.loads(r.text))[1]['bedroom']==3)
    assert ((json.loads(r.text))[1]['bathroom']==5)
    assert ((json.loads(r.text))[1]['pool']==0)
    assert ((json.loads(r.text))[1]['jacuzzi']==1)
    assert ((json.loads(r.text))[1]['nb_equip']==25)
    assert (type((json.loads(r.text))[1]['result'])==float)
    assert (type((json.loads(r.text))[1]['predictions.date'])==str)
    assert (type((json.loads(r.text))[1]['production_models.date'])==str)


 
