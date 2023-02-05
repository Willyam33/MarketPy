from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import access 
import log
import data_manipulation 
import database_functions
import new_model_golive
import datetime
import pandas as pd
import properties
from joblib import load
import uvicorn
import asyncio

pool_possible_values = 3
jacuzzi_possible_values = 2

class Input(BaseModel):
    """ Classe décrivant les caractéritiques du logement à estimer """
    rating:float
    tag:str
    bedroom:int
    bathroom:int
    pool:int
    jacuzzi:int
    nb_equip:int

api = FastAPI(
    title="API for Pricing Rental Prediction",
    description="Predicting the pricing of a holiday rental with inputs",
    version="1.0.0"
)

def mapping_like_sqlachemy(results,columns=""):
    # Dictionnary - Ready for API
    dict_results = []
    if columns == "":
        for dict_row in results.mappings():
            dict_results.append(dict_row)
    else:
        columns_list=columns.split(", ")
        # Not pretty good method, but troubles encountered in managing results from Alchemy
        if (type(results)==list):
            results_list=results
        else:
            results_list=results.fetchall()
        for result in results_list:
            dict_row=dict(zip(columns_list,result))
            dict_results.append(dict_row)   
    return dict_results


def manage_access_control(access_control):
    if access_control['status']==access.ERROR:
        raise HTTPException(status_code=500, detail=access_control['error_code'])
    elif access_control['status']==access.DENIED:
        raise HTTPException(status_code=401, detail=access_control['error_code'])

@api.get('/', name="Vérify API is UP")
def get_index():
    """
    Returns API UP...
    """
    print("API UP")
    return 'API UP...'

@api.post('/predict', name="Predict price")
def predict(
        input: Input,
        username=Header(None, description='user login'), 
        password=Header(None, description='user password')):
    """
    Doing prediction
    """

    """ Access control """
    manage_access_control(access.verify_user_access(username,password))

    """ Coherency control """
    if ( (input.bathroom > 10 or input.bathroom < 0) or
         (input.bedroom > 10 or input.bedroom < 0) or
         (input.tag != "" and input.tag != "Superhôte") or
         (input.pool > 2 or input.pool < 0) or
         (input.jacuzzi > 1 or input.jacuzzi < 0) or
         (input.nb_equip > 40 or input.nb_equip <0) ):
        return log.error_messages['NOT_IN_RANGE']

    data=pd.DataFrame({
        'rating': input.rating,
        'bedroom': input.bedroom,
        'bathroom': input.bathroom,
        'nb_equip': input.nb_equip},index=[0])
    
    for i in range(pool_possible_values):
        data['pool_'+str(i)]=0
    data['tag_Pas de tag']=0
    data['tag_Superhôte']=0
    for i in range(jacuzzi_possible_values):
        data['jacuzzi_'+str(i)]=0

    if input.tag=="Superhôte":
        data['tag_Superhôte']=1
    else:
        data['tag_Pas de tag']=1

    for i in range(jacuzzi_possible_values):
        if input.jacuzzi==i:
            data['jacuzzi_'+str(i)]=1

    for i in range(pool_possible_values):
        if input.pool==i:
            data['pool_'+str(i)]=1

    status, production_model_id = database_functions.get_production_model_id()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    elif production_model_id!=0:
        # Getting production pipeline 
        try:
            pipeline=load(properties.model_folder+properties.model_file)
        except:
            return log.error_messages['MODEL_NOT_FOUND']

        """ Predicting """
        prediction=data_manipulation.predict(pipeline,data)[0]

        """ Saving Prediction in the database """
        status, prediction_id = database_functions.save_prediction_metadata(
            date_prm = datetime.datetime.now().strftime("%d-%b-%Y-%H:%M:%S"), 
            model_id_prm = production_model_id,
            user_id_prm = database_functions.get_user_id(username)[1],
            rating_prm = input.rating,
            tag_prm = input.tag,
            bedroom_prm = input.bedroom,
            bathroom_prm = input.bathroom,
            pool_prm = input.pool,
            jacuzzi_prm = input.jacuzzi,
            nb_equip_prm = input.nb_equip,
            result_prm = prediction)

        return prediction
    else:
        return log.error_messages['NO_MODEL_IN_PRODUCTION']

@api.get('/predictions/{username_who_did_predictions}', name="Get predictions")
def get_predictions(
        username_who_did_predictions: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Getting predictions done by an identified user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    status, results=database_functions.get_predictions_for_user(username_who_did_predictions)
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        dict_results=mapping_like_sqlachemy(results)
        if len(dict_results)==0:
            return log.warning_messages['NO_PREDICTION_FOR_USER']+username_who_did_predictions
        else:
            return dict_results

@api.get('/predictions_details/{username_who_did_predictions}', name="Get predictions and model details for an identified user")
def get_predictions_details(
        username_who_did_predictions: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Getting predictions done by an identified user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    status, results=database_functions.get_predictions_details_for_user(username_who_did_predictions)
    columns=database_functions.get_predictions_details_columns()

    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        dict_results=mapping_like_sqlachemy(results,columns)
        if len(dict_results)==0:
            return log.warning_messages['NO_PREDICTION_FOR_USER']+username_who_did_predictions
        else:
            return dict_results

@api.get('/predictions', name="Get predictions")
def get_predictions(
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Getting all predictions occured, with models and users informations
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    status, results=database_functions.get_all_predictions()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        dict_results=mapping_like_sqlachemy(results)
        if len(dict_results)==0:
            return log.warning_messages['NO_PREDICTION']
        else:
            return dict_results

@api.get('/golive_decision_informations', name="Get all informations in order to decide for new model to go live")
def get_golive_desicion_informations(
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Getting all informations needed to decide for new model to go live
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    datasets = {}
    scorings = {}
    production_model = {}

    """ Getting last dataset """
    status, results=database_functions.get_last_valid_dataset()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        datasets=mapping_like_sqlachemy(results)
        if len(datasets)==0:
            dataset = { 'dataset_warning' : log.warning_messages['NO_VALID_DATASET_AVAILABLE'] }
        else:
            dataset = datasets[0] 
            """ Getting models scoring for last dataset """
            status, results=database_functions.get_models_scoring_for_dataset(datasets[0]['id'])
            if status=='KO':
                raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
            else:
                scorings=mapping_like_sqlachemy(results)
                if len(scorings)==0:
                    scorings = { 'scoring_warning' : log.warning_messages['NO_SCORED_MODEL_FOR_THE_LAST_VALID_DATASET'] }
    
    """ Getting production model informations """
    status, results=database_functions.get_production_model_informations()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        if status == 'NO_MODEL_IN_PRODUCTION':
            production_model = { 'production_model_warning' : log.warning_messages['NO_MODEL_IN_PRODUCTION'] }
        else:
            production_model=mapping_like_sqlachemy(results,database_functions.get_production_model_informations_columns())[0]

    return { 'dataset' : dataset,
             'scorings' : scorings,
             'production_model' : production_model }

@api.post('/new_model_golive', name="new model deployment command")
def post_new_model_golive(
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Deployment of a new model
    Can only MEP best model selected from last scoring on last valid dataset
    If there is no scoring, MEP is impossible
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Verifying conditions : """
    """ Getting last valid dataset """
    status, results=database_functions.get_last_valid_dataset()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        datasets=mapping_like_sqlachemy(results)
        if len(datasets)==0:
            return log.warning_messages['NO_VALID_DATASET_AVAILABLE'] 
   
    """ Getting the best model for the found dataset """
    status, results=database_functions.get_best_model_for_dataset(datasets[0]['id'])
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        scorings=mapping_like_sqlachemy(results)
        if len(scorings)==0:
            return log.warning_messages['NO_SCORED_MODEL_FOR_THE_LAST_VALID_DATASET'] 

    """ Training and Saving Pipeline """
    status, message = new_model_golive.train_and_save_pipeline(scorings[0]['model_library'],
                                                               scorings[0]['model_name'], 
                                                               datasets[0]['id'],
                                                               datasets[0]['name'])
    if status=='KO':
        raise HTTPException(status_code=500, detail=message)
    else:
        return message

@api.delete('/delete_user/{username_to_delete}', name="Delete user from database")
def delete_user(
        username_to_delete: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Deleting user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Coherency control """
    status, users_username = database_functions.get_users_username()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else :
        if username_to_delete not in users_username:
            return log.error_messages['USER_UNKNOWN']

    status=database_functions.delete_user(username_to_delete)
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        return username_to_delete+log.success_messages['USER_DELETED']

@api.put('/add_user/{username_to_add}/{password_to_add}', name="Add user to database")
def add_user(
        username_to_add: str,
        password_to_add: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Adding new user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Coherency control """
    status,users_username=database_functions.get_users_username()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    elif username_to_add in users_username:
        return username_to_add+log.error_messages['USER_ALREADY_EXISTS']

    status,results=database_functions.add_user(username_to_add,password_to_add)
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        return username_to_add+log.success_messages['USER_ADDED']

@api.delete('/delete_model/{model}', name="Delete model from database")
def delete_model(
        model: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Deleting user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Coherency control """
    status,models_name=database_functions.get_models_name()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    elif model not in models_name:
        return model+log.error_messages['MODEL_UNKNOWN']

    status=database_functions.delete_model(model)
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        return model+log.success_messages['MODEL_DELETED']

@api.put('/add_model/{library}/{model}', name="Add model template to database")
def add_model(
        library: str,
        model: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Adding new model
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Coherency control """
    status,models_name=database_functions.get_models_name()
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR']) 
    elif model in models_name:
        return model+log.error_messages['MODEL_ALREADY_IN_BASE']

    status,results=database_functions.add_model(library,model)
    if status=='KO':
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        return model+log.success_messages['MODEL_ADDED']

server = None

@api.get("/shutdown_async")
async def shutdown(
    username=Header(None, description='admin login'), 
    password=Header(None, description='admin password')):
    """
    Shutting down API - admin access requires
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    global server

    server.should_exit = True
    server.force_exit = True
    await server.shutdown()

def launching_API():
    global server
    config = uvicorn.Config("api:api", host="127.0.0.1", port=properties.port_API_uvicorn, log_level="info")
    server = uvicorn.Server(config)
    server.run()
