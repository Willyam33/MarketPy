import os
import sys
import pytest
import requests
import json
import test_properties

from test_functions import alter_table, un_alter_table

# Test of api.py
url_root = 'http://127.0.0.1:'+test_properties.port_API_uvicorn

############################
# API Test for adding user #
############################

def test_add_user_ok():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters "user3","pass3"
    # return HTTPCode 200,"user3 a été ajouté.e"

    endpoint="/add_user"
    parameters="/user3/pass3"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"user3 a été ajouté.e !"')

def test_add_user_already_exists():

    # Error Test Case : User already exists
    # header : username="admin", password="admin"
    # parameters "user3","pass3"
    # return HTTPCode 200,"user3 existe déjà !"

    endpoint="/add_user"
    parameters="/user3/pass3"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"user3 existe déjà !"')

def test_add_user_on_corrupted_database():

    # Error Test Case : Database is corrupted (table name)
    # header : username="admin", password="admin"
    # parameters "user4", "pass4"
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('users')

    endpoint="/add_user"
    parameters="/user4/pass4"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("users")

def test_add_user_not_admin():

    # Error Test Case : User doing demand is not admin (DB UP again)
    # header : username="user1", password="pass1"
    # parameters "user4", "pass4"
    # return HTTPCode 401,"L'utilisateur n'est pas administrateur !"
    
    endpoint="/add_user"
    parameters="/user4/pass4"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "user1",
                              "password": "pass1"}) 

    assert ((json.loads(r.text))['detail']=='L utilisateur n est pas administrateur !')
    assert (r.status_code==401)

def test_add_user_bad_password():
    # Error Test Case : Admin password is wrong
    # header : username="admin", password="admi"
    # parameters "user4", "pass4"
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    endpoint="/add_user"
    parameters="/user4/pass4"
    r = requests.put(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admi"}) 

    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)

##############################
# API Test for deleting user #
##############################

def test_delete_user_ok():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters "user3"
    # return HTTPCode 200,"user3 a été supprimé.e"

    endpoint="/delete_user"
    parameters="/user3"
    r = requests.delete(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"user3 a été supprimé.e !"')

def test_delete_user_unknown():

    # Error Test Case : User doesn't exist
    # header : username="admin", password="admin"
    # parameters "user3"
    # return HTTPCode 200,"L utilisateur n'existe pas !"

    endpoint="/delete_user"
    parameters="/user3"
    r = requests.delete(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert (r.text=='"L utilisateur n existe pas !"')

def test_delete_user_on_corrupted_database():

    # Error Test Case : Database is corrupted (table name)
    # header : username="admin", password="admin"
    # parameters "user2"
    # return HTTPCode 500,"Erreur d accès à la base de données"
    
    alter_table('users')

    endpoint="/delete_user"
    parameters="/user2"
    r = requests.delete(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table("users")


def test_delete_user_not_admin():

    # Error Test Case : User doing demand is not admin (DB UP again)
    # header : username="user1", password="pass1"
    # parameters "user2"
    # return HTTPCode 401,"L utilisateur n'est pas administrateur !"
    
    endpoint="/delete_user"
    parameters="/user2"
    r = requests.delete(url=url_root+endpoint+parameters,
                     headers={"username": "user1",
                              "password": "pass1"}) 

    assert ((json.loads(r.text))['detail']=='L utilisateur n est pas administrateur !')
    assert (r.status_code==401)

def test_delete_user_bad_password():
    # Error Test Case : Admin password is wrong
    # header : username="admin", password="admi"
    # parameters "user2"
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    endpoint="/delete_user"
    parameters="/user2"
    r = requests.delete(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admi"}) 

    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)

