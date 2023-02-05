import sys
import os
import environment_deploy

project_path=str(os.environ.get("MARKETPY_PATH"))

# path for libraries depending on environment (DEV/QA/PREPROD/DEMO/PROD/)
sys.path.append(project_path+"/"+environment_deploy.environment+"/python_files")

# Port depending on environment 
port_API_uvicorn=environment_deploy.port_API_uvicorn