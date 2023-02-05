import os
import sys
import pytest
import deploy_properties
import database_deployments

# Alive test of database

def test_DB_UP():

    # Normal Test Case
    # return Status 'OK', Result "DB UP..."
    status, result = database_deployments.database_alive_test()
    assert (status=='OK')
    assert (result=='DB UP...' )