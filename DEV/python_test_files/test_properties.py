# Global variables used for testing

import sys
import os
import environment_test

project_path=str(os.environ.get("MARKETPY_PATH"))

# dataset used for testing folder
dataset_test_folder = project_path+"/"+environment_test.environment+"/test_files/" 

# path for operational libraries depending on environment (DEV/QA/PREPROD/DEMO/PROD/)
sys.path.append(project_path+"/"+environment_test.environment+"/python_files")

# static port for API uvicorn server, depends on environment
port_API_uvicorn=environment_test.port_API_uvicorn

# static IP for MySQL server, depends on environment
MySQL_IP=environment_test.MySQL_IP
