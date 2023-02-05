#!bin/sh

# Deploying application - Python code

if [ "$#" -ne 1 -o "$1" != "DEV" -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" -a "$1" != "PROD" ]; then 
    echo "Usage: install_deployment_py_files.sh [environment]" 
    echo "La pré-installation des fichiers de déploiement n'a pas été réalisée en "$1
    echo ""
    exit 1
else
    echo "Pré-installation des fichiers de déploiement en "$1 
    MARKETPY_PATH="/home/ubuntu/MarketPy"

    # Creating Pre installation File Tree
    if [ "$1" != "DEV" ]; then
        mkdir $MARKETPY_PATH/PROV
        cp -r $MARKETPY_PATH/DEV/python_deploy_files $MARKETPY_PATH/PROV
        cp $MARKETPY_PATH/config/environment_deploy_$1.py $MARKETPY_PATH/PROV/python_deploy_files/environment_deploy.py
    fi
    echo "Pré-installation effectuée en "$1 
    echo ""
    exit 0
fi
