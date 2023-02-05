import sqlalchemy
from sqlalchemy.engine import create_engine
import test_properties
import properties
import shutil
import database_deployments

# Preparing database for testing
database_deployments.drop_database()
database_deployments.create_database()
 
   

