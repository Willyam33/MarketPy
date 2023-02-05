import pytest
import os
from test_functions import copy_of_csv_file_from_test_folder_to_incoming_folder, alter_table, un_alter_table
import test_properties
import properties
import database_functions
import listen_to_dataset_arrival

# Testing application behavior on database corruption 

def test_listening_workflow_database_table_dataset_ko():
    ''' Listing and catching valid CSV file but table dataset KO in database
    '''
    
    # Altering datasets table
    alter_table('datasets')

    # Copying a valid CSV file in Incoming Folder
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid4.csv")
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
    assert('valid4.csv' in files)

    # Isolated files folder
    path=properties.isolated_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert('valid1.csv' in files)
    assert('valid2.csv' in files)

    ### Checking Database ###

    # Checking Table datasets

    status, datasets_results=database_functions.get_all_datasets()
    assert(status=='KO')

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
    assert(len(dict_production_models_results)==1)
    assert(dict_production_models_results[0]['id']==1)
    assert(type(dict_production_models_results[0]['date'])==str)
    assert(dict_production_models_results[0]['version']=='V1.0')
    assert(dict_production_models_results[0]['name']=='LinearRegression')
    assert(type(dict_production_models_results[0]['scores'])==str)
    assert(dict_production_models_results[0]['dataset_scoring_ids']=="2")
    assert(dict_production_models_results[0]['remove_date']==None)

    # Retablishing table datasets
    un_alter_table('datasets')

#test_listening_workflow_database_table_dataset_ko()

def test_listening_workflow_database_table_scoring_ko():
    ''' Listing and catching valid CSV file but table scoring KO on database
    '''
    
    # Altering scoring table
    alter_table('scoring')

    # Copying a valid CSV file in Incoming Folder
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid4.csv")
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
    assert('valid4.csv' in files)

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
    assert(len(dict_datasets_results)==4) # Assuming Dataset is recorded even if scoring recording is impossible

    # Checking Table scoring

    status, scoring_results=database_functions.get_all_scorings()

    assert(status=='KO')

    # Checking Table production_model

    status, production_models_results=database_functions.get_all_production_models()
    dict_production_models_results = []
    for dict_production_models_row in production_models_results.mappings():
        dict_production_models_results.append(dict_production_models_row)

    assert(status=='OK')
    assert(len(dict_production_models_results)==1)
    assert(dict_production_models_results[0]['id']==1)
    assert(type(dict_production_models_results[0]['date'])==str)
    assert(dict_production_models_results[0]['version']=='V1.0')
    assert(dict_production_models_results[0]['name']=='LinearRegression')
    assert(type(dict_production_models_results[0]['scores'])==str)
    assert(dict_production_models_results[0]['dataset_scoring_ids']=="2,4")
    assert(dict_production_models_results[0]['remove_date']==None)

    # Retablishing table scoring
    un_alter_table('scoring')

#test_listening_workflow_database_table_scoring_ko()

def test_listening_workflow_database_table_models_ko():
    ''' Listing and catching valid CSV file but table models and production models KO on database
    '''
    
    # Altering models table
    alter_table('models')
    alter_table('production_models')

    # Copying a valid CSV file in Incoming Folder
    copy_of_csv_file_from_test_folder_to_incoming_folder("valid5.csv")
    listen_to_dataset_arrival.listening_workflow()

    # Incoming files folder
    path=properties.incoming_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    assert(len(files)==0)

    # Raw files folder
    path=properties.raw_files_folder
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    print([f for f in files])
    assert('valid5.csv' in files)
    assert('invalid.csv' in files)
    assert('valid.csv' in files)
    assert('valid3.csv' in files)
    assert('valid4.csv' in files)

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
    assert(len(dict_datasets_results)==5) # Assuming Dataset is recorded even if models used to score are unavailable

    # Checking Table scoring
 
    status, scoring_results=database_functions.get_all_scorings()
    assert(status=='OK')

    # Checking Table production_model

    status, production_models_results=database_functions.get_all_production_models()
    assert(status=='KO')

    # Retablishing table models and production_models
    un_alter_table('models')
    un_alter_table('production_models')
