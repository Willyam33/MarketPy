from sqlalchemy.engine import create_engine
import datetime
import log
import properties


# By convention, -1 is used for error return code

# creating a connection to the database
# mysql_url = 'my_mysql' 
mysql_url = properties.MySQL_IP 
mysql_user = 'root'
mysql_password = 'msq3!xAk3c'  
database_name = ''

# recreating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# creating the connection
mysql_engine = create_engine(connection_url)

############################# GENERIC FUNCITONS #############################################

def get_elements_from_select(command:str):
    ''' Executing mysql sqlalchemy engine with select command
        Parameters
            SQL command
        Returns 
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''
    try:
        with mysql_engine.connect() as connection:
            results=connection.execute(command)
            return 'OK', results
    except :
        return 'KO', None

def set_elements_for_insert(command:str):
    ''' Executing mysql sqlalchemy engine with insert command
        Parameters
            SQL command
        Returns 
            status : 'OK' / 'KO'
            last row id if status is OK, 0 else
    '''
    try:
        with mysql_engine.connect() as connection:
            lastrowid=connection.execute(command).lastrowid
            return 'OK', lastrowid
    except :
        return 'KO', 0

def set_elements_for_update(command:str):
    ''' Executing mysql sqlalchemy engine with update command
        Parameters
            SQL command
        Returns 
            status : 'OK' / 'KO'
    '''
    try:
        with mysql_engine.connect() as connection:
            connection.execute(command)
        return 'OK'
    except :
        return 'KO'

def delete_elements(command:str):
    ''' Deleting elements
        Parameters
            SQL command
        Returns 
            status : 'OK' / 'KO'
    '''
    try:
        with mysql_engine.connect() as connection:
            results=connection.execute(command)
        return 'OK'
    except :
        return 'KO'


############################# DATASET METADATA ACCESS #######################################

def save_new_dataset_metadata(filename_prm:str,
                              date_prm:str,
                              invalid_prm:bool,
                              size_before_cleaning_prm:int,
                              size_after_cleaning_prm:int):
    ''' Saving new dataset metadata
        Parameters
            dataset filename
            collect date
            validity of the dataset
            size before cleaning (number of lines)
            size after cleaning (number of lines)
        Returns 
            status : 'OK' / 'KO'
            last row id if status is OK, 0 else
    '''

    if invalid_prm:
        command = \
            'INSERT INTO marketPyDB.datasets (name, import_date, invalid, size_before_cleaning, size_after_cleaning) VALUES \
            ("{filename}","{date}",{invalid},{size_before_cleaning},{size_after_cleaning});'.format(
                filename=filename_prm,
                date=date_prm,
                invalid=1,
                size_before_cleaning = 0,
                size_after_cleaning = 0
            )
    else:
        command = \
            'INSERT INTO marketPyDB.datasets (name, import_date, invalid, size_before_cleaning, size_after_cleaning) VALUES \
            ("{filename}","{date}",{invalid},{size_before_cleaning},{size_after_cleaning});'.format(
                filename=filename_prm,
                date=date_prm,
                invalid=0,
                size_before_cleaning = size_before_cleaning_prm,
                size_after_cleaning = size_after_cleaning_prm
        )
 
    return set_elements_for_insert(command)

def get_last_valid_dataset():
    ''' Getting last valid dataset
        No Parameters
        Returns 
            status : 'OK' / 'KO'
            dataset_id and dataset_name if status is OK, None else
    '''

    command = 'SELECT id, name FROM marketPyDB.datasets WHERE invalid=0 ORDER BY id DESC;' 
 
    return get_elements_from_select(command)

############################# MODEL METADATA ACCESS #######################################

def save_new_production_model_metadata(date_prm:str,
                                       version_prm:str,
                                       name_prm:str,
                                       scores_prm:str,
                                       dataset_scoring_ids_prm:str):
    ''' Saving new production model metadata
        Parameters
            golive date for this production model
            version X.Y (X = new model, Y = new training)
            name of the model
            scores (evolutes during the production time)
            datests ids used for scoring (during the production time)
        Returns 
            status : 'OK' / 'KO'
            last row id if status is OK, 0 else
    '''

    command = \
        'INSERT INTO marketPyDB.production_models (date, version, name, scores, dataset_scoring_ids) VALUES  \
        ("{date}","{version}","{name}","{scores}","{dataset_scoring_ids}");'.format(
            date=date_prm,
            version=version_prm,
            name=name_prm,
            scores = scores_prm,
            dataset_scoring_ids = dataset_scoring_ids_prm
        )
    return set_elements_for_insert(command)

def save_prediction_metadata(date_prm:str,
                             model_id_prm:int,
                             user_id_prm:int,
                             rating_prm:float,
                             tag_prm:str,
                             bedroom_prm:int,
                             bathroom_prm:int,
                             pool_prm:int,
                             jacuzzi_prm:int,
                             nb_equip_prm:int,
                             result_prm:float):
    ''' Recording prediction, features and user id
        Parameters : All parameters required for a prediction
        Returns -1 if error, else last row id
    '''

    command = \
        'INSERT INTO marketPyDB.predictions (date, model_id, user_id, rating, tag, bedroom, bathroom, pool, jacuzzi, nb_equip, result) VALUES  \
        ("{date}",{model_id},{user_id},{rating},"{tag}",{bedroom},{bathroom},{pool},{jacuzzi},{nb_equip},{result});'.format(
            date=date_prm,
            model_id=model_id_prm,
            user_id=user_id_prm,
            rating = rating_prm,
            tag = tag_prm,
            bedroom = bedroom_prm,
            bathroom = bathroom_prm,
            pool = pool_prm,
            jacuzzi = jacuzzi_prm,
            nb_equip = nb_equip_prm,
            result = result_prm           
        )
    return set_elements_for_insert(command)

################### PRODUCTION MODEL METADATA ACCESS #######################################

def get_production_model_informations(command=""):
    ''' Getting production model informations
        Parameters : SQL command
            (the production model is identified by a remove date as null)
        Returns 
            status : 'OK' / 'KO' / 'NO_MODEL_IN_PRODUCTION'
            results if status is OK, None else
    '''
    if command=="":
        command='SELECT * FROM marketPyDB.production_models WHERE remove_date IS NULL;'
    status, results=get_elements_from_select(command)
    if status=='KO':
        return 'KO', None
    else:
        results_list=results.fetchall()
        if len(results_list)==0:
            return 'NO_MODEL_IN_PRODUCTION', None 
        elif len(results_list)>1:
            log.error("DATABASE_INCONSISTENCY")
            return 'KO', None 
        else:
            return 'OK', results_list
            
def get_production_model_informations_columns():
    ''' Used for mapping like a Result.mappings() in sqlaclchemy library for joint tables
        No parameters 
        Returns columns name for mapping
    '''
    return "id, date, version, name, scores, dataset_scoring_ids, remove_date"

def get_production_model_id():
    ''' Getting the production model id
        No parameters (the production model is identified by a remove date as null)
        Returns 
            status : 'OK' / 'KO' / 'NO_MODEL_IN_PRODUCTION'
            model id if status is OK, 0 else
    '''

    command = 'SELECT id FROM marketPyDB.production_models WHERE remove_date IS NULL;'
    status, results=get_production_model_informations(command)
    if (status!='OK'):
        return status, 0
    else:
        return status, results[0][0]

def get_production_model_version_and_name():
    ''' Getting the production model version and name
        No parameters (the production model is identified by a remove date as null)
        Returns 
            status : 'OK' / 'KO' / 'NO_MODEL_IN_PRODUCTION'
            model database id if status is OK, 0 else
            model version if status is OK, "" else
            model nameif status is OK, "" else
    '''
    
    command = 'SELECT id, version, name FROM marketPyDB.production_models WHERE remove_date IS NULL;'
    status, results=get_production_model_informations(command)
    if (status!='OK'):
        return status, 0, "", ""
    else:
        return status, results[0][0], results[0][1], results[0][2]

def get_production_model_scoring():
    ''' Getting the production model version and name
        No parameters (the production model is identified by a remove date as null)
        Returns 
            status : 'OK' / 'KO' / 'NO_MODEL_IN_PRODUCTION'
            model database id if status is OK, 0 else
            model version if status is OK, ""0"" else
            model nameif status is OK, "" else
    '''
    
    command = 'SELECT id, scores, dataset_scoring_ids FROM marketPyDB.production_models WHERE remove_date IS NULL;'
    status, results=get_production_model_informations(command)
    if (status!='OK'):
        return status, 0, "", ""
    else:
        return status, results[0][0], results[0][1], results[0][2]

def remove_model_from_production(model_id_prm:int,date_prm:str):
    ''' Removing the production model means indicating a remove date on current production model
        Parameters 
            Model production id
            Date (Present date by default)
        Returns 
            status : 'OK' / 'KO'
    '''
    if (date_prm == ""):
        remove_date_prm = datetime.datetime.now().strftime("%d-%b-%Y-%H:%M:%S")
    else:
        remove_date_prm = date_prm

    command = 'UPDATE marketPyDB.production_models SET remove_date="{remove_date}" WHERE id={model_id};'.format(
        model_id=model_id_prm,
        remove_date=remove_date_prm   
    )
    return set_elements_for_update(command)

def set_production_model_scoring(model_id_prm:int,scores_prm:str,dataset_scoring_ids_prm:str):
    ''' Setting new score for production model
        Parameters 
            Model production id
            Scores
            Dataset used for scoring
        Returns 
            status : 'OK' / 'KO'
    '''
    command = 'UPDATE marketPyDB.production_models SET scores="{scores}", dataset_scoring_ids="{dataset_scoring_ids}" WHERE id={model_id};'.format(
        model_id=model_id_prm,
        scores=scores_prm,   
        dataset_scoring_ids=dataset_scoring_ids_prm   
    )
    return set_elements_for_update(command)

############################# MODEL METADATA ACCESS #######################################

def get_models_name():
    ''' Getting models name
        No Parameters
        Returns
            status : 'OK' / 'KO' / 'NO_MODEL_IN_DATABASE'
            model names if status is OK, None else
    '''

    command = 'SELECT name FROM marketPyDB.models;'
    status, results = get_elements_from_select(command)
    if (status=='KO'):
        return status, None
    else:
        results_list=results.fetchall()
        if len(results_list)==0:
            return 'NO_MODEL_IN_DATABASE', None
        else:
            return status, ([item[0] for item in results_list])

def add_model(library_prm,name_prm):
    ''' Adding new model
        Parameters
            python machine learning library name
            machine learning model name
        Returns
            status : 'OK' / 'KO'
            last row id if status is OK, 0 else
    '''
    command = 'INSERT INTO marketPyDB.models (name, library) VALUES ("{name}","{library}");'.format(
        name=name_prm,
        library=library_prm
    )
    return set_elements_for_insert(command)

def delete_model(name_prm):
    ''' Deleting a model
        Parameters
            machine learning model name
        Returns
            status : 'OK' / 'KO'
    '''

    command = 'DELETE FROM marketPyDB.models WHERE name="{name}";'.format(
        name=name_prm,
    )
    return delete_elements(command)

############################# USER METADATA ACCESS #######################################

def get_password(username_prm):
    ''' Getting password for user
        Parameters
            user's username
        Returns
            status : 'OK' / 'KO'
            password if 'OK', else None
    '''

    command = 'SELECT password FROM marketPyDB.users WHERE username="{username}";'.format(
        username=username_prm
    )
    status, results = get_elements_from_select(command)
    if (status == 'KO'):
        return status, None
    else:
        return status, results.fetchall()[0][0]

def get_users_username():
    ''' Getting users username
        No parameters
        Returns
            status : 'OK' / 'KO' / 'NO_MODEL_IN_DATABASE'
            model names if status is OK, None else
    '''
    
    command = 'SELECT username FROM marketPyDB.users;'
    status, results = get_elements_from_select(command)
    if (status=='KO'):
        return status, None
    else:
        results_list=results.fetchall()
        if len(results_list)==0:
            return 'NO_USER_IN_DATABASE', None
        else:
            return status, ([item[0] for item in results_list])

def get_user_id(username_prm):
    ''' Getting users username
        Parameters
            user's username
        Returns
            status : 'OK' / 'KO'
            user_id if 'OK', else 0
    '''

    command = 'SELECT id FROM marketPyDB.users WHERE username="{username}";'.format(
        username=username_prm
    )
    status, results = get_elements_from_select(command)
    if (status=='KO'):
        return status, 0
    else:
        return status, results.fetchall()[0][0]

def add_user(username_prm,password_prm):
    ''' Adding user
        Parameters
            user's username
            user's password
        Returns
            status : 'OK' / 'KO'
            last row id if status is OK, 0 else
    '''
    command = 'INSERT INTO marketPyDB.users (username, password) VALUES ("{username}","{password}");'.format(
        username=username_prm,
        password=password_prm
    )
    return set_elements_for_insert(command)

def delete_user(username_prm):
    ''' Deleting user
        Parameters
            user's username
        Returns
            status : 'OK' / 'KO'
    '''

    command = 'DELETE FROM marketPyDB.users WHERE username="{username}";'.format(
        username=username_prm,
    )
    return delete_elements(command)

####################### PREDICTION METADATA ACCESS ###########################################

def get_predictions_for_user(username_prm):
    ''' Getting predictions for a user
        Parameters
            user's username
        Returns
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''

    command = 'SELECT date, model_id, rating, tag, bedroom, bathroom, pool, jacuzzi, nb_equip, result \
               FROM marketPyDB.predictions LEFT JOIN marketPyDB.users ON marketPyDB.predictions.user_id = marketPyDB.users.id \
               WHERE username="{username}";'.format(
        username=username_prm
    )
    return (get_elements_from_select(command))

def get_predictions_details_for_user(username_prm):
    ''' Getting detailed predictions, included production models metadata, for a user
        Parameters
            user's username
        Returns
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''

    command = 'SELECT {predictions_details_columns} \
               FROM marketPyDB.predictions LEFT JOIN marketPyDB.users ON marketPyDB.predictions.user_id = marketPyDB.users.id \
               LEFT JOIN marketPyDB.production_models ON marketPyDB.predictions.model_id = marketPyDB.production_models.id \
               WHERE username="{username}";'.format(
        username=username_prm,
        predictions_details_columns=get_predictions_details_columns()
    )
    return (get_elements_from_select(command))

def get_predictions_details_columns():
    ''' Used for mapping because of dysfonctionnement of Result.mappings() in sqlaclchemy library for joint tables
        No parameters 
        Returns columns name for mapping
    '''    
    return "predictions.id, predictions.date, model_id, production_models.date, version, name, rating, tag, bedroom, bathroom, pool, jacuzzi, nb_equip, result"

############################# SCORING ACCESS #######################################

def save_models_scoring_on_new_dataset(
                              model_list_prm,
                              score_list_prm:float,
                              dataset_id_prm:int,
                              best_model_index_prm:int):
    ''' Saving new scorings on new dataset
        Parameters
            model list scored (access by index)
            scores list (same indexing as model list)  
            dataset id used for scoring
            best model identification
        Returns
            status : 'OK' / 'KO'
            last row id if status is OK, 0 else
    '''
    command=""
    for i in range(len(model_list_prm)):
        if i==best_model_index_prm:
            best_model_int=1
        else:
            best_model_int=0

        command = command + \
            'INSERT INTO marketPyDB.scoring (model_name, model_library, score, dataset_id, best_model) VALUES \
            ("{model_name}","{model_library}",{score},{dataset_id},{best_model});'.format(
                model_name = model_list_prm[i]['name'],
                model_library = model_list_prm[i]['library'],
                score = score_list_prm[i],
                dataset_id = dataset_id_prm,
                best_model = best_model_int)
 
    return set_elements_for_insert(command)

def get_best_model_for_dataset(dataset_id_prm:int):
    ''' Getting models scoring informations for a dataset
        Parameters 
            dataset identification in the database
        Returns
            status : 'OK' / 'KO'
            last row id if status is OK, 0 else
    '''
    command = 'SELECT id, model_library, model_name FROM marketPyDB.scoring WHERE dataset_id={dataset_id} AND best_model=1;'.format(
                dataset_id = dataset_id_prm)
 
    return get_elements_from_select(command)

def get_models_scoring_for_dataset(dataset_id_prm:int):
    ''' Getting models scoring informations for a dataset
        Parameters
            dataset identification in the database
        Returns
            status : 'OK' / 'KO'
            last row id if status is OK, 0 else
    '''
    command = 'SELECT id, model_library, model_name, score, best_model FROM marketPyDB.scoring WHERE dataset_id={dataset_id};'.format(
                dataset_id = dataset_id_prm)
 
    return get_elements_from_select(command)


####################### FULL ACCESS ###########################################

def get_all_predictions():
    ''' Getting all predictions
        No parameters
        Returns 
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''

    command = 'SELECT * FROM marketPyDB.predictions;'
    status, results = get_elements_from_select(command)
    return (status, results)

def get_all_models():
    ''' Getting all models
        No parameters
        Returns 
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''

    command = 'SELECT * FROM marketPyDB.models;'
    status, results = get_elements_from_select(command)
    return (status, results)

def get_all_production_models():
    ''' Getting all production models
        No parameters
        Returns 
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''

    command = 'SELECT * FROM marketPyDB.production_models;'
    status, results = get_elements_from_select(command)
    return (status, results)

def get_all_datasets():
    ''' Getting all datasets
        No parameters
        Returns 
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''

    command = 'SELECT * FROM marketPyDB.datasets;'
    status, results = get_elements_from_select(command)
    return (status, results)

def get_all_users(): 
    ''' Getting all users
        No parameters
        Returns 
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''

    command = 'SELECT * FROM marketPyDB.users;'   
    status, results = get_elements_from_select(command)
    return (status, results.fetchall())
    
def get_all_scorings(): 
    ''' Getting all scorings
        Returns 
            status : 'OK' / 'KO'
            results if status is OK, None else
    '''

    command = 'SELECT * FROM marketPyDB.scoring;'   
    status, results = get_elements_from_select(command)
    return (status, results)

