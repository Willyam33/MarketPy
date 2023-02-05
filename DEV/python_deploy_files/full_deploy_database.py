import os
import sys
import pytest
import deploy_properties
import database_deployments

def test_full_deploy_database(): 
    ''' Full database deployment - Used for the first deployment of MarketPy Application
    '''
    status = database_deployments.create_database()
    assert (status=='OK')
