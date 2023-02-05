#!bin/sh

# API alive testing

# Waiting between each retry.
retry_time=10
i=0
if [ "$#" -ne 2 -o "$1" -gt 11 -o "$1" -lt 1 -o "$2" != 'DEV' -a "$2" != "QA" -a "$2" != "DEMO" -a "$2" != "PREPROD" -a "$2" != "PROD" ]; then 
    echo "Usage: test.sh [nombre entre 1 et 10] [environment (DEV/QA/DEMO/PREPROD/PROD)]" 
    echo "Le test de disponibilité de la base de données n'a pas été lancé"
    echo ""
    exit 1
else
    export MARKETPY_PATH="/home/ubuntu/MarketPy"
    echo " failed by default" > resultats.txt
    # Technical tests for availability of API.
    while [ $i -lt "$1" ]
    do 
        i=$(($i + 1))
        echo "Tests de disponibilité de l'API : Essai numéro "$i
        python3 -m pytest $MARKETPY_PATH/PROV/python_deploy_files/alive_test_API.py > resultats.txt # overwriting at each run
        if [ $(grep " failed" resultats.txt | wc -l) -eq 0 ]; then
            echo "Tests de disponibilité de l'API OK"
            echo ""
            exit 0
        fi
        if [ "$i" -eq $1 ]; then
            sleep 1
            echo "Tests de disponibilité de l'API KO"
            echo ""
            exit 1
        fi
        echo "KO - Nouvel essai dans "$retry_time" secondes"
        sleep $retry_time
    done

fi