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

def create_database():
    ''' This method is used for the first deployment of the MarketPy Product
        No Parameters
        Returns
            Status OK / KO
    '''
    try:
        with mysql_engine.connect() as connection:
            connection.execute('CREATE DATABASE IF NOT EXISTS marketPyDB;')
            connection.execute('CREATE TABLE IF NOT EXISTS marketPyDB.datasets ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    name VARCHAR(64), \
                                    import_date VARCHAR(64), \
                                    invalid INT, \
                                    size_before_cleaning INT, \
                                    size_after_cleaning INT);')
            connection.execute('CREATE TABLE IF NOT EXISTS marketPyDB.production_models ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    date VARCHAR(32), \
                                    version VARCHAR(8), \
                                    name VARCHAR(64), \
                                    scores VARCHAR(64), \
                                    dataset_scoring_ids VARCHAR(64), \
                                    remove_date VARCHAR(32));')
            connection.execute('CREATE TABLE IF NOT EXISTS marketPyDB.models ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    name VARCHAR(32), \
                                    library VARCHAR(64));')
            connection.execute('DELETE FROM marketPyDB.models;')
            connection.execute('INSERT INTO marketPyDB.models (name, library) VALUES ("LinearRegression","sklearn.linear_model");')
            connection.execute('INSERT INTO marketPyDB.models (name, library) VALUES ("DecisionTreeRegressor","sklearn.tree");')
            connection.execute('INSERT INTO marketPyDB.models (name, library) VALUES ("RandomForestRegressor","sklearn.ensemble");')
            connection.execute('CREATE TABLE IF NOT EXISTS marketPyDB.predictions ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    date VARCHAR(64), \
                                    model_id INT, \
                                    user_id INT, \
                                    rating FLOAT, \
                                    tag VARCHAR(64), \
                                    bedroom INT, \
                                    bathroom INT, \
                                    pool INT, \
                                    jacuzzi INT, \
                                    nb_equip INT, \
                                    result FLOAT);')
            connection.execute('CREATE TABLE IF NOT EXISTS marketPyDB.users ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    username VARCHAR(64), \
                                    password VARCHAR(64));')
            connection.execute('DELETE FROM marketPyDB.users;')
            connection.execute('INSERT INTO marketPyDB.users (username, password) VALUES ("admin","admin");')
            connection.execute('INSERT INTO marketPyDB.users (username, password) VALUES ("user1","pass1");')
            connection.execute('INSERT INTO marketPyDB.users (username, password) VALUES ("user2","pass2");')
            connection.execute('CREATE TABLE IF NOT EXISTS marketPyDB.scoring ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    model_library VARCHAR(64), \
                                    model_name VARCHAR(32), \
                                    score FLOAT, \
                                    dataset_id INT, \
                                    best_model INT);')
        return 'OK'
    except:
        return 'KO'

def drop_database():
    ''' This shouldn't be used
        No Parameters
        Returns
            Status OK / KO
    '''
    try:
        with mysql_engine.connect() as connection:
            connection.execute('DROP DATABASE marketPyDB;')
        return 'OK'
    except :
        return 'KO'

def modify_database():
    ''' This method is used by deployement pipelines in order to update the database scheme
        No Parameters
        Returns
            Status OK / KO
    '''
    try:
        #with mysql_engine.connect() as connection:
            #connection.execute('Type here your SQL commands')
            #connection.execute('')
            #.....
            #connection.execute
        return 'OK'
    except :
        return 'KO'

def database_alive_test():
    ''' This method is used by deployment pipeline in order to know if database is up :)
        No Parameters
        Returns
            Status OK / KO
    '''
    try:
        with mysql_engine.connect() as connection:
            connection.execute('CREATE DATABASE IF NOT EXISTS technical_test;')
            connection.execute('CREATE TABLE technical_test.content ( id INT PRIMARY KEY AUTO_INCREMENT, \
                                                                     name VARCHAR(32) );')
            connection.execute('INSERT INTO technical_test.content (name) VALUES ("DB UP...");')
            results = connection.execute('SELECT * FROM technical_test.content;')
            connection.execute('DROP DATABASE technical_test;')
        return 'OK', results.fetchall()[0][1]
    except :
        return 'KO', ""
