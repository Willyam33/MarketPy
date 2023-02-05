import pytest
import os
from test_functions import copy_of_csv_file_from_test_folder_to_incoming_folder, alter_table, un_alter_table
import test_properties
import properties
import database_functions
import listen_to_dataset_arrival

# Testing listeing workflow, one valid dataset, several valid datasets, one invalid dataset

def test_listening_workflow_ok():
    ''' Listing and catching valid CSV file
    '''
    
    #Copy a valid CSV file in Incoming Folder
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid.csv")
    
    listen_to_dataset_arrival.listening_workflow()

    ### Checking FileSystem ###

    # Incoming files folder
    path=properties.incoming_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert(len(files)==0)

    # Raw files folder
    path=properties.raw_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert(files[0]=='valid.csv')

    # Isalated files folder
    path=properties.isolated_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert(len(files)==0)

    ### Checking Database ###

    # Checking Table datasets

    status, datasets_results=database_functions.get_all_datasets()
    dict_datasets_results = []
    for dict_datasets_row in datasets_results.mappings():
        dict_datasets_results.append(dict_datasets_row)

    assert(status=='OK')
    assert(len(dict_datasets_results)==1)
    assert(dict_datasets_results[0]['id']==1)
    assert(dict_datasets_results[0]['name']=='valid.csv')
    assert(type(dict_datasets_results[0]['import_date'])==str)
    assert(dict_datasets_results[0]['invalid']==0)
    assert(dict_datasets_results[0]['size_before_cleaning']==5243)
    assert(dict_datasets_results[0]['size_after_cleaning']==4252)

    # Checking Table scoring

    status, scoring_results=database_functions.get_all_scorings()
    dict_scoring_results = []
    for dict_scoring_row in scoring_results.mappings():
        dict_scoring_results.append(dict_scoring_row)

    assert(status=='OK')
    assert(len(dict_scoring_results)==3)
    assert(dict_scoring_results[0]['id']==1)
    assert(dict_scoring_results[0]['model_library']=='sklearn.linear_model')
    assert(dict_scoring_results[0]['model_name']=='LinearRegression')
    assert(type(dict_scoring_results[0]['score'])==float)
    assert(dict_scoring_results[0]['dataset_id']==1)
    assert(dict_scoring_results[0]['best_model']==1)
    assert(dict_scoring_results[1]['id']==2)
    assert(dict_scoring_results[1]['model_library']=='sklearn.tree')
    assert(dict_scoring_results[1]['model_name']=='DecisionTreeRegressor')
    assert(type(dict_scoring_results[1]['score'])==float)
    assert(dict_scoring_results[1]['dataset_id']==1)
    assert(dict_scoring_results[1]['best_model']==0)
    assert(dict_scoring_results[2]['id']==3)
    assert(dict_scoring_results[2]['model_library']=='sklearn.ensemble')
    assert(dict_scoring_results[2]['model_name']=='RandomForestRegressor')
    assert(type(dict_scoring_results[2]['score'])==float)
    assert(dict_scoring_results[2]['dataset_id']==1)
    assert(dict_scoring_results[2]['best_model']==0)

    # Checking Table scoring

    status, production_models_results=database_functions.get_all_production_models()
    dict_production_models_results = []
    for dict_production_models_row in production_models_results.mappings():
        dict_production_models_results.append(dict_production_models_row)

    assert(status=='OK')
    assert(len(dict_production_models_results)==0)

#test_listening_workflow_ok()

def test_listening_workflow_3_files():
    ''' Listing and catching valid 3 CSV files
    '''    

    #Copy a valid CSV file in Incoming Folder
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid1.csv")
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid2.csv")
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid3.csv")

    listen_to_dataset_arrival.listening_workflow()

    ### Checking FileSystem ###

    # Incoming files folder
    path=properties.incoming_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert(len(files)==0)

    # Raw files folder
    path=properties.raw_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert('valid3.csv' in files)

    # Isalated files folder
    path=properties.isolated_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert('valid1.csv' in files)
    assert('valid2.csv' in files)

    ### Checking Database ###

    # Checking Table datasets

    status, datasets_results=database_functions.get_all_datasets()
    dict_datasets_results = []
    for dict_datasets_row in datasets_results.mappings():
        dict_datasets_results.append(dict_datasets_row)

    assert(status=='OK')
    assert(len(dict_datasets_results)==2)
    assert(dict_datasets_results[0]['id']==1)
    assert(dict_datasets_results[0]['name']=='valid.csv')
    assert(type(dict_datasets_results[0]['import_date'])==str)
    assert(dict_datasets_results[0]['invalid']==0)
    assert(dict_datasets_results[0]['size_before_cleaning']==5243)
    assert(dict_datasets_results[0]['size_after_cleaning']==4252)
    assert(dict_datasets_results[1]['id']==2)
    assert(dict_datasets_results[1]['name']=='valid3.csv')
    assert(type(dict_datasets_results[1]['import_date'])==str)
    assert(dict_datasets_results[1]['invalid']==0)
    assert(dict_datasets_results[1]['size_before_cleaning']==4188)
    assert(dict_datasets_results[1]['size_after_cleaning']==3379)
 
     # Checking Table scoring

    status, scoring_results=database_functions.get_all_scorings()
    dict_scoring_results = []
    for dict_scoring_row in scoring_results.mappings():
        dict_scoring_results.append(dict_scoring_row)

    assert(status=='OK')
    assert(len(dict_scoring_results)==6)
    assert(dict_scoring_results[0]['id']==1)
    assert(dict_scoring_results[0]['model_library']=='sklearn.linear_model')
    assert(dict_scoring_results[0]['model_name']=='LinearRegression')
    assert(type(dict_scoring_results[0]['score'])==float)
    assert(dict_scoring_results[0]['dataset_id']==1)
    assert(dict_scoring_results[0]['best_model']==1)
    assert(dict_scoring_results[1]['id']==2)
    assert(dict_scoring_results[1]['model_library']=='sklearn.tree')
    assert(dict_scoring_results[1]['model_name']=='DecisionTreeRegressor')
    assert(type(dict_scoring_results[1]['score'])==float)
    assert(dict_scoring_results[1]['dataset_id']==1)
    assert(dict_scoring_results[1]['best_model']==0)
    assert(dict_scoring_results[2]['id']==3)
    assert(dict_scoring_results[2]['model_library']=='sklearn.ensemble')
    assert(dict_scoring_results[2]['model_name']=='RandomForestRegressor')
    assert(type(dict_scoring_results[2]['score'])==float)
    assert(dict_scoring_results[2]['dataset_id']==1)
    assert(dict_scoring_results[2]['best_model']==0)
    assert(dict_scoring_results[3]['id']==4)
    assert(dict_scoring_results[3]['model_library']=='sklearn.linear_model')
    assert(dict_scoring_results[3]['model_name']=='LinearRegression')
    assert(type(dict_scoring_results[3]['score'])==float)
    assert(dict_scoring_results[3]['dataset_id']==2)
    assert(dict_scoring_results[3]['best_model']==1)
    assert(dict_scoring_results[4]['id']==5)
    assert(dict_scoring_results[4]['model_library']=='sklearn.tree')
    assert(dict_scoring_results[4]['model_name']=='DecisionTreeRegressor')
    assert(type(dict_scoring_results[4]['score'])==float)
    assert(dict_scoring_results[4]['dataset_id']==2)
    assert(dict_scoring_results[4]['best_model']==0)
    assert(dict_scoring_results[5]['id']==6)
    assert(dict_scoring_results[5]['model_library']=='sklearn.ensemble')
    assert(dict_scoring_results[5]['model_name']=='RandomForestRegressor')
    assert(type(dict_scoring_results[5]['score'])==float)
    assert(dict_scoring_results[5]['dataset_id']==2)
    assert(dict_scoring_results[5]['best_model']==0)

    # Checking Table production_model

    status, production_models_results=database_functions.get_all_production_models()
    dict_production_models_results = []
    for dict_production_models_row in production_models_results.mappings():
        dict_production_models_results.append(dict_production_models_row)

    assert(status=='OK')
    assert(len(dict_production_models_results)==0)

#test_listening_workflow_3_files()

def test_listening_workflow_invalid():
    ''' Listing and catching invalid CSV file
    '''
    
    #Copy a valid CSV file in Incoming Folder
    copy_of_csv_file_from_test_folder_to_incoming_folder("invalid.csv")
    
    listen_to_dataset_arrival.listening_workflow()

    # Incoming files folder
    path=properties.incoming_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert(len(files)==0)

    # Raw files folder
    path=properties.raw_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert('invalid.csv' in files)
    assert('valid.csv' in files)
    assert('valid3.csv' in files)

    # Isalated files folder
    path=properties.isolated_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert('valid1.csv' in files)
    assert('valid2.csv' in files)

    ### Checking Database ###

    # Checking Table datasets

    status, datasets_results=database_functions.get_all_datasets()
    dict_datasets_results = []
    for dict_datasets_row in datasets_results.mappings():
        dict_datasets_results.append(dict_datasets_row)

    assert(status=='OK')
    assert(len(dict_datasets_results)==3)
    assert(dict_datasets_results[0]['id']==1)
    assert(dict_datasets_results[0]['name']=='valid.csv')
    assert(type(dict_datasets_results[0]['import_date'])==str)
    assert(dict_datasets_results[0]['invalid']==0)
    assert(dict_datasets_results[0]['size_before_cleaning']==5243)
    assert(dict_datasets_results[0]['size_after_cleaning']==4252)
    assert(dict_datasets_results[1]['id']==2)
    assert(dict_datasets_results[1]['name']=='valid3.csv')
    assert(type(dict_datasets_results[1]['import_date'])==str)
    assert(dict_datasets_results[1]['invalid']==0)
    assert(dict_datasets_results[1]['size_before_cleaning']==4188)
    assert(dict_datasets_results[1]['size_after_cleaning']==3379)
    assert(dict_datasets_results[2]['id']==3)
    assert(dict_datasets_results[2]['name']=='invalid.csv')
    assert(type(dict_datasets_results[2]['import_date'])==str)
    assert(dict_datasets_results[2]['invalid']==1)
    assert(dict_datasets_results[2]['size_before_cleaning']==0)
    assert(dict_datasets_results[2]['size_after_cleaning']==0)

     # Checking Table scoring

    status, scoring_results=database_functions.get_all_scorings()
    dict_scoring_results = []
    for dict_scoring_row in scoring_results.mappings():
        dict_scoring_results.append(dict_scoring_row)

    assert(status=='OK')
    assert(len(dict_scoring_results)==6)

    # Checking Table production_model

    status, production_models_results=database_functions.get_all_production_models()
    dict_production_models_results = []
    for dict_production_models_row in production_models_results.mappings():
        dict_production_models_results.append(dict_production_models_row)

    assert(status=='OK')
    assert(len(dict_production_models_results)==0)

#test_listening_workflow_invalid()

