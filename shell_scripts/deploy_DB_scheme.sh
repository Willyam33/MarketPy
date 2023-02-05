#!bin/sh

# Deploying database scheme (Full or Delta)

if [ "$#" -ne 2 -o "$2" != "--db_full" -a "$2" != "--db_delta" -o "$1" != "DEV" -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" -a "$1" != "PROD" ]; then 
    echo "test.sh [environment (DEV/QA/DEMO/PREPROD/PROD)] [--db_full/--db_delta]" 
    exit 1
else
    export MARKETPY_PATH="/home/ubuntu/MarketPy"
    echo " failed by default" > resultats.txt

    if [ "$2" = "--db_full" ]; then
        echo "Déploiement du schéma de la base de données en full"
        python3 -m pytest $MARKETPY_PATH/$1/python_deploy_files/full_deploy_database.py > resultats.txt
        #python3 $MARKETPY_PATH/$1/python_deploy_files/full_deploy_database.py
    else
        echo "Déploiement du schéma de la base de données en delta"
        python3 -m pytest $MARKETPY_PATH/$1/python_deploy_files/delta_deploy_database.py > resultats.txt
        #python3 $MARKETPY_PATH/$1/python_deploy_files/delta_deploy_database.py
    fi
    if [ $(grep " no tests ran" resultats.txt | wc -l) -eq 0 -a $(grep " failed" resultats.txt | wc -l) -eq 0 -a $(grep " error" resultats.txt | wc -l) -eq 0 ]; then
        echo "Le déploiement du schéma a réussi."
        echo ""
        exit 0
    else
        echo "Le déploiement du schéma a échoué."
        echo ""
        exit 1 
    fi
fi

