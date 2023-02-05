import sqlalchemy
from sqlalchemy.engine import create_engine
import test_properties
import properties
import shutil

# Creating connection parameters to the database
mysql_url = test_properties.MySQL_IP 
mysql_user = 'root'
mysql_password = 'msq3!xAk3c'  
database_name = ''

# Creating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user, 
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# Creating the connection
mysql_engine = create_engine(connection_url)

# Simulating database alteration for users table
def alter_table(table_name):
    try:
        with mysql_engine.connect() as connection:
            connection.execute('ALTER TABLE marketPyDB.'+table_name+' RENAME TO marketPyDB.'+table_name+'_bidon;')
    except:
        print("Erreur dans le protocole de test : Echec de l'alteration de table")

def un_alter_table(table_name):
    try:
        with mysql_engine.connect() as connection:
            connection.execute('ALTER TABLE marketPyDB.'+table_name+'_bidon RENAME TO marketPyDB.'+table_name+';')
    except:
        print("Erreur dans le protocole de test : Echec de l'alteration de table")

# Copying files from test dataset repository to incoming datasets folder
def copy_of_csv_file_from_test_folder_to_incoming_folder(filename):
    try:
        print(test_properties.dataset_test_folder+filename)
        print(properties.incoming_files_folder+filename)
        shutil.copy(test_properties.dataset_test_folder+filename,
                    properties.incoming_files_folder+filename)
    except:
        print("Erreur dans le protocole de test : Echec de la copie de fichier")
   

