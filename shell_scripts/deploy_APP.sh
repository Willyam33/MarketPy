#!bin/sh

# Deploying application - Python code

if [ "$#" -ne 1 -o "$1" != "DEV" -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" -a "$1" != "PROD" ]; then 
    echo "Usage: deploy_APP.sh [environment]" 
    echo "Le déploiement applicatif n'a pas été réalisé en "$1
    echo ""
    exit 1
else
    echo "Déploiement du code applicatif en "$1 
    export MARKETPY_PATH="/home/ubuntu/MarketPy"

    # Creating File Tree
    rm -r $MARKETPY_PATH/$1
    mkdir $MARKETPY_PATH/$1
    mkdir $MARKETPY_PATH/$1/raw_files/
    mkdir $MARKETPY_PATH/$1/incoming_files/
    mkdir $MARKETPY_PATH/$1/isolated_files/
    mkdir $MARKETPY_PATH/$1/model

    if [ "$1" != "PROD" ]; then
        mkdir $MARKETPY_PATH/$1/test_files/
    fi
    
    # Copying Files
    if [ "$1" = "DEV" ]; then
        # Faire un git pull
        cp $MARKETPY_PATH/config/environment_test_$1.py $MARKETPY_PATH/$1/python_test_files/environment_test.py
    else
        cp -r $MARKETPY_PATH/DEV/python_files $MARKETPY_PATH/$1/
        cp -r $MARKETPY_PATH/DEV/python_deploy_files $MARKETPY_PATH/$1/
        if [ $1 != "PROD" ]; then
            cp -r $MARKETPY_PATH/DEV/python_test_files $MARKETPY_PATH/$1/
            cp $MARKETPY_PATH/config/environment_test_$1.py $MARKETPY_PATH/$1/python_test_files/environment_test.py
            cp $MARKETPY_PATH/DEV/test_files/* $MARKETPY_PATH/$1/test_files/
        fi
    fi

    cp $MARKETPY_PATH/config/environment_$1.py $MARKETPY_PATH/$1/python_files/environment.py
    cp $MARKETPY_PATH/config/environment_deploy_$1.py $MARKETPY_PATH/$1/python_deploy_files/environment_deploy.py
    
    echo "Le déploiement applicatif a été réalisé en "$1
    echo ""
    exit 0

fi