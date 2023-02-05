import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sklearn
import datetime

from joblib import dump
import database_functions
import data_manipulation
import properties 
import log

def manage_versionning(version,production_model_name,new_model_name):
    ''' Managin version number X.Y (X : new model type, Y : new training on new dataset)
        Parameters
            present version V<X.Y>
            production model name
            new model name
        Return
            new version V<X'.Y'>
    '''
    # Deformating version
    x,y=version[1:].split('.')
    # If new and old model name are not the same
    if production_model_name!=new_model_name:
        # Then updating first number
        x=int(x)+1
        y=0
    else:
        # Else updating second number
        y=int(y)+1
    # Formating version
    return ("V"+str(x)+"."+str(y))

def train_and_save_pipeline(model_library, model_name, dataset_id, dataset_name):
    ''' Train model and save it
        Parameters
            python machine learning library name
            machine learning model name
            dataset identification in the database
            dataset name
        Returns
            status OK/KO
            detailed message
    '''
    # With dataset_id, find dataset and set features and target
    # Reading csv in raw files folder and extracting data
    df=data_manipulation.get_dataframe_from_file(dataset_name,
                                                 properties.raw_files_folder)
        
    # Cleaning and Preparing data
    cleaned_df=data_manipulation.clean_data(df)

    # Preparing for training
    features,target=data_manipulation.prepare_for_training(cleaned_df)
    
    # Training and scoring
    status, pipeline, score = data_manipulation.train_and_score_model(model_library, model_name, features, target)
    if status!='OK':
        return 'KO',log.error_messages[status]

    # Updating production model metadata (version and name)
    date = datetime.datetime.now().strftime("%d-%b-%Y-%H:%M:%S")
    status, production_model_id, production_model_version, production_model_name = \
        database_functions.get_production_model_version_and_name()

    if (status=='KO'):
        return 'KO',log.error_messages['DATABASE_ERROR']

    if (production_model_id==0): # If production model doesn't exists, Then 
        new_version="V1.0"
    else:
        # Removing current version 
        status=database_functions.remove_model_from_production(production_model_id,date)
        if status=='KO':
            return 'KO', log.error_messages['DATABASE_ERROR']
        # Creating new version
        new_version = manage_versionning(production_model_version,production_model_name,model_name) 

    # Managing scores and dataset used for training
    scores=format(score, ".2f")
    dataset_scoring_ids=str(dataset_id)

    # Saving pipeline file
    try:
        dump(pipeline, properties.model_folder+properties.model_file)
    except:
        return 'KO', log.error_messages['UNABLE_TO_SAVE_PRODUCTION_PIPELINE_FILE']+" "+log.warning_messages['NO_MODEL_IN_PRODUCTION']       

    # Saving in Database
    status=database_functions.save_new_production_model_metadata(
        date_prm=date,
        version_prm=new_version,
        name_prm=model_name,
        scores_prm=scores,
        dataset_scoring_ids_prm=dataset_scoring_ids)
    if status=='KO':
        return 'KO', log.error_messages['DATABASE_ERROR']+" "+log.warning_messages['NO_MODEL_IN_PRODUCTION']   
    else:
        return 'OK', log.success_messages['NEW_MODEL_IN_PRODUCTION']




