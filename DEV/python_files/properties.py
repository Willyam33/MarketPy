# Global variables

import os
import environment

# absolute path
project_path=str(os.environ.get("MARKETPY_PATH"))

# incoming dataset files folder
incoming_files_folder = project_path+"/"+environment.environment+"/incoming_files/" 

# selected dataset files for training folder
raw_files_folder = project_path+"/"+environment.environment+"/raw_files/" 

# directory for isolated data files
isolated_files_folder = project_path+"/"+environment.environment+'/isolated_files/' 

# directory for production machine learning trained models
model_folder = project_path+"/"+environment.environment+'/model/'

# name of production machine learning trained model
model_file = 'model.pckl'

# period for checking new dataset arrival
listening_period=environment.listening_period 

# static IP for MySQL server, depends on environment
MySQL_IP=environment.MySQL_IP

# static port for API uvicorn server, depends on environment
port_API_uvicorn=environment.port_API_uvicorn
