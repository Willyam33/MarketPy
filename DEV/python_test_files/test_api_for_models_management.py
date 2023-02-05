import pytest
import requests
import json
from test_functions import alter_table, un_alter_table
import test_properties

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

#############################
# API Test for adding model #
#############################

def test_add_model_ok():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters "sklearn.neural_network", "MLPRegressor"
    # return HTTPCode 200,"MLPRegressor a été ajouté.e"

    endpoint="/add_model"
    parameters="/sklearn.neural_network/MLPRegressor"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"MLPRegressor a été ajouté !"')

def test_add_model_already_exists():

    # Error Test Case : Model already exists
    # header : username="admin", password="admin"
    # parameters "sklearn.neural_network", "MLPRegressor"
    # return HTTPCode 200,"MLPRegressor est déjà enregistré et disponible en base !"

    endpoint="/add_model"
    parameters="/sklearn.neural_network/MLPRegressor"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"MLPRegressor est déjà enregistré et disponible en base !"')

def test_add_model_and_corrupted_users_table():

    # Error Test Case : Database is corrupted (users table name)
    # header : username="admin", password="admin"
    # parameters "sklearn.neural_network", "MLPRegressor"
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('users')

    endpoint="/add_model"
    parameters="/sklearn.neural_network/MLPRegressor"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("users")

def test_add_model_and_corrupted_models_table():

    # Error Test Case : Database is corrupted (models table name)
    # header : username="admin", password="admin"
    # parameters "sklearn.neural_network", "MLPRegressor"
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('models')

    endpoint="/add_model"
    parameters="/sklearn.neural_network/MLPRegressor"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("models")

def test_add_model_not_admin():

    # Error Test Case : User doing demand is not admin (DB UP again)
    # header : username="user1", password="pass1"
    # parameters "sklearn.neural_network", "MLPRegressor"
    # return HTTPCode 401,"L'utilisateur n'est pas administrateur !"
    
    endpoint="/add_model"
    parameters="/sklearn.neural_network/MLPRegressor"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "user1",
                              "password": "pass1"}) 

    assert ((json.loads(r.text))['detail']=='L utilisateur n est pas administrateur !')
    assert (r.status_code==401)

def test_add_model_bad_password():
    # Error Test Case : Admin password is wrong
    # header : username="admin", password="admi"
    # parameters "sklearn.neural_network", "MLPRegressor"
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    endpoint="/add_model"
    parameters="/sklearn.neural_network/MLPRegressor"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admi"}) 

    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)

##############################
# API Test for deleting model #
##############################

def test_delete_model_ok():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters "MLPRegressor"
    # return HTTPCode 200,"MLPRegressor a été supprimé.e"

    endpoint="/delete_model"
    parameters="/MLPRegressor"
    r = requests.delete(url=url_root+endpoint+parameters,
                        headers={"username": "admin",
                                 "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"MLPRegressor a été supprimé !"')

def test_delete_model_unknown():

    # Error Test Case : Model doesn't exist
    # header : username="admin", password="admin"
    # parameters "MLPRegressor"
    # return HTTPCode 200,"Le modèle n'existe pas en base!"

    endpoint="/delete_model"
    parameters="/MLPRegressor"
    r = requests.delete(url=url_root+endpoint+parameters,
                        headers={"username": "admin",
                                 "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"MLPRegressor n existe pas en base !"')

def test_delete_model_and_corrupted_users_table():

    # Error Test Case : Database is corrupted (users table name)
    # header : username="admin", password="admin"
    # parameters "MLPRegressor"
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('users')

    endpoint="/delete_model"
    parameters="/MLPRegressor"
    r = requests.delete(url=url_root+endpoint+parameters,
                        headers={"username": "admin",
                                 "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("users")

def test_delete_model_and_corrupted_models_table():

    # Error Test Case : Database is corrupted (models table name)
    # header : username="admin", password="admin"
    # parameters "MLPRegressor"
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('models')

    endpoint="/delete_model"
    parameters="/MLPRegressor"
    r = requests.delete(url=url_root+endpoint+parameters,
                        headers={"username": "admin",
                                 "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("models")

def test_delete_models_not_admin():

    # Error Test Case : User doing demand is not admin (DB UP again)
    # header : username="user1", password="pass1"
    # parameters "MLPRegressor"
    # return HTTPCode 401,"L utilisateur n est pas administrateur !"
    
    endpoint="/delete_model"
    parameters="/MLPRegressor"
    r = requests.delete(url=url_root+endpoint+parameters,
                        headers={"username": "user1",
                                 "password": "pass1"}) 

    assert ((json.loads(r.text))['detail']=='L utilisateur n est pas administrateur !')
    assert (r.status_code==401)

def test_delete_model_bad_password():
    # Error Test Case : Admin password is wrong
    # header : username="admin", password="admi"
    # parameters "MLPRegressor"
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    endpoint="/delete_model"
    parameters="/MLPRegressor"
    r = requests.delete(url=url_root+endpoint+parameters,
                        headers={"username": "admin",
                                 "password": "admi"}) 

    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)
