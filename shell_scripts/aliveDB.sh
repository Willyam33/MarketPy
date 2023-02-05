#!bin/sh

# DB alive testing

# Waiting between each retry.
retry_time=10

if [ "$#" -ne 1 -o "$1" != 'DEV' -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" -a "$1" != "PROD" ]; then 
    echo "Usage: test.sh [environment (DEV/QA/DEMO/PREPROD/PROD)]" 
    echo "Le test de disponibilité de la base de données n'a pas été lancé"
    echo ""
    exit 1
else
    export MARKETPY_PATH="/home/ubuntu/MarketPy"
    echo " failed by default" > resultats.txt
    # Technical tests for availability of the database.
    for i in `seq 1 10`; do 
        echo "Tests de disponibilité de la base de données : Essai numéro "$i
        python3 -m pytest $MARKETPY_PATH/$1/python_deploy_files/alive_test_DB.py > resultats.txt # overwriting at each run
        if [ $(grep " failed" resultats.txt | wc -l) -eq 0 ]; then
            echo "Tests de disponibilité de la base de données OK"
            echo ""
            exit 0
        fi
        if [ "$i" -eq 10 ]; then
            echo "Tests de disponibilité de la base de données KO"
            echo ""
            exit 1
        fi
        echo "KO - Nouvel essai dans "$retry_time" secondes"
        sleep $retry_time
    done

fi
