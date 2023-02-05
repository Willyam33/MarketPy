import properties
import os
import log
import time
import numpy as np
import datetime
import shutil
import data_manipulation 
import database_functions
from joblib import load

def is_there_new_file():
    ''' Checking if new files are in the incoming files folder
        No parameters
        Returns
            Status OK/KO
            Filenames
            Which file is last arrived
    '''
    path = properties.incoming_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    if len(files)==0:
        # No file in directory
        return 'KO', "", 0
    elif len(files)==1:
        # One file
        return 'OK', files, 0
    else:
        # Serveral files, only last is returned
        modification_times=[]
        for f in files:
            modification_times.append(os.stat(os.path.join(path, f)).st_mtime)
        return 'OK', files, np.argmax(modification_times)

def dispatch_files(catched_files, index_of_selected_file):
    ''' Collecting selected file, Isolating others
        Parameters
            files found in incoming files folder
            index of which one to keep
        No returns
            TODO : Exception management on copy errors
    '''
    for i in range(len(catched_files)):
        if i == index_of_selected_file:
            shutil.move(properties.incoming_files_folder+catched_files[i],
                        properties.raw_files_folder+catched_files[i])
        else:
            shutil.move(properties.incoming_files_folder+catched_files[i],
                        properties.isolated_files_folder+catched_files[i])

def store_dataset_metadata(filename:str,df,cleaned_df):
    ''' Saving dataset metadata in database even if invalid
        Parameters
            dataset filename
            dataframe before cleaning
            dataframe after cleaning
        Returns dataset database id, 'KO' if error
    '''
    date = datetime.datetime.now().strftime("%d-%b-%Y-%H:%M:%S")

    if (cleaned_df.empty): # Dataset is empty, means a problem occured during cleaning : Warning
        log.warning('INVALID_DATASET')
        status, dataset_id=database_functions.save_new_dataset_metadata(filename,
                                                                date_prm=date,
                                                                invalid_prm=True,
                                                                size_before_cleaning_prm=0,
                                                                size_after_cleaning_prm=0)
        if status=='KO': 
            log.error('UNABLE_TO_SAVE_DATASET_METADATA') 
            return status, 0 
        else:
            return status, dataset_id # Dataset is invalid
    else:
        status, dataset_id=database_functions.save_new_dataset_metadata(filename,
                                                                date_prm=date,
                                                                invalid_prm=False,
                                                                size_before_cleaning_prm=len(df),
                                                                size_after_cleaning_prm=len(cleaned_df))
        if status=='KO':
            log.error('UNABLE_TO_SAVE_DATASET_METADATA')
            return status, 0
        else: # Dataset is valid, the show must go on
            log.success('DATASET_OK')
            return status, dataset_id

def find_the_best_model(features,target,dataset_id):
    ''' Finding the best model, in databases's models, for the new dataset
        Parameters 
            features, 
            target
        No returns
    '''

    #Scaling data
    features_scaled=data_manipulation.scaler_transformation(features)
    
    #Getting models from database
    model_score_list=[]
    status, results=database_functions.get_all_models()
         
    if status=='KO': # Means there is a problem to get models from database
        log.error('UNABLE_TO_GET_MODELS_FOR_TRAINING_AND_SCORING')
    else:
        model_list=results.fetchall()
        if len(model_list)==0:
            log.warning('NO_MODEL_AVAILABLE_FOR_TRAINING_AND_SCORING')
        else:
            #Scoring models
            for model in model_list:
                status, score=data_manipulation.compute_model_score(model,features_scaled,target)
                if status=='OK':
                    model_score_list.append(score)
                else:
                    log.error(status,model['name'])
                    break

            if status=='OK':
                best_model_index=np.argmax(model_score_list)
                best_model_name=(model_list[best_model_index])['name']
                log.success('BEST_MODEL_IS',best_model_name)

                #Recording in database
                status, results=database_functions.save_models_scoring_on_new_dataset(model_list,model_score_list,dataset_id,best_model_index)
                if status=='KO':
                    log.error('UNABLE_TO_SAVE_SCORING_IN_DATABASE')
                else:            
                    log.success('MODEL_SCORING_FOR_NEW_DATASET_RECORDED')
                  
def predict_and_score_on_production_pipeline(features, target, dataset_id):
    ''' Predicting and scoring 
        Parameters
            features
            target
            dataset identification in the database
        No returns
    '''
    # Getting production model scorings
    status, production_model_id, production_model_scores, production_model_dataset_scoring_ids = \
        database_functions.get_production_model_scoring()

    if (status=='KO'):
        log.error('UNABLE_TO_MANAGE_PRODUCTION_MODELS')
    elif production_model_id==0:
        log.warning('NO_MODEL_IN_PRODUCTION')
    else:
        # Getting production pipeline 
        try:
            pipeline=load(properties.model_folder+properties.model_file)
        except Exception as e:
            log.error('UNABLE_TO_LOAD_PRODUCTION_PIPELINE_FILE')
            return

        # Predicting and scoring pipeline
        score=data_manipulation.predict_and_score_pipeline(pipeline,features,target)
    
        # Saving scoring in the database
        status=database_functions.set_production_model_scoring(
            model_id_prm=production_model_id,
            scores_prm=production_model_scores+','+format(score, ".2f"), 
            dataset_scoring_ids_prm=production_model_dataset_scoring_ids+','+str(dataset_id)
        )
        if status=='KO':
            log.error('UNABLE_TO_SAVE_PRODUCTION_SCORING_ON_NEW_DATASET')
        else:
            log.success('PRODUCTION_SCORING_UPDATED') 

def listening_workflow():
    ''' Workflow manager
        No parameters
        No returns
    '''
    try:
        status, catched_files, index_of_selected_file = is_there_new_file()
    except:
        log.error('FILE_SYSTEM_TROUBLE_IN_LOOKING_FOR_NEW_DATASETS')
        return 'KO'

    if status=='OK':
    
        # File move from incoming files folder to raw files folder or isolated files folder
        try:
            dispatch_files(catched_files, index_of_selected_file)
        except :
            log.error('FILE_SYSTEM_TROUBLE_IN_DISPATCHING_DATASETS_FILES')
            return 'KO'
        
        log.success('NEW_INCOMING_FILE_FOUND')
       
        filename=catched_files[index_of_selected_file]

        # Reading csv in raw files folder and extracting data
        df=data_manipulation.get_dataframe_from_file(filename,
                                                     properties.raw_files_folder)
        
        # Cleaning and Preparing data
        cleaned_df=data_manipulation.clean_data(df)
        
        # Storing dataset metadata
        status, dataset_id=store_dataset_metadata(filename,df,cleaned_df)

        if (cleaned_df.empty == False) and (status == 'OK'): 

            #Preparing for training
            features,target=data_manipulation.prepare_for_training(cleaned_df)
            
            #Finding the best model for the new dataset
            find_the_best_model(features,target,dataset_id) 

            # Predicting and scoring on production model in order to evaluate deviation
            # Realized on unscaled features because the pipeline makes the scaling    
            predict_and_score_on_production_pipeline(features, target, dataset_id)

def listening():
    ''' Entry point for catching new datasets in incoming files folder
        Calling Workflow manager with listening period
        No parameters
        No returns
    '''
    while True:

        # Listening
        log.information('LISTENING',datetime.datetime.now().strftime("%d-%b-%Y-%H:%M:%S"))

        listening_workflow()
 
        log.information('NEXT_LISTENING_IN',str(properties.listening_period))
        time.sleep(properties.listening_period)