#!bin/sh

# Tagging GIT -> Pull Request on DEV -> Deploying QA -> Launching QA Servers (API and MySQL) -> Testing -> If OK -> GO LIVE

if [ "$#" -ne 3 -o "$2" != 'DEV' -a "$2" != "QA" -a "$2" != "PREPROD"  -a "$2" != "DEMO" -a "$2" != "PROD" -o "$3" != '--db_delta' -a "$3" != "--db_full" -a "$3" != "--no_db_update" ]
then 
    echo "releaseEnv.sh [Version_Tag] [ENVIRONMENT (DEV/QA/DEMO/PREPROD/PROD)] --db_full" 
    echo "releaseEnv.sh [Version_Tag] [ENVIRONMENT (DEV/QA/DEMO/PREPROD/PROD)] --db_delta"
    echo "releaseEnv.sh [Version_Tag] [ENVIRONMENT (DEV/QA/DEMO/PREPROD/PROD)] --no_db_update"
else
    export MARKETPY_PATH=/home/ubuntu/MarketPy
    # Tagging GIT

    # Pull Request on DEV

    # Installation of deployment python files
    sh install_deployment_py_files.sh $2

    # Disponibility API vérification (1 retry)
    sh aliveAPI.sh 1 $2
    if [ "$?" -eq 0 ]; then 
        # Shutting down the API
        sh shutdownAPI.sh $2
    else
        echo "Pas d'API à éteindre"
        echo ""
    fi
    sleep 2

    # Shutting down Dataset Collect process if alive
    sh shutdownDatasetCollect.sh $2
    sleep 2

    # Deploying application in QA environment
    sh deploy_APP.sh $2
    if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    sleep 2
    
    # Launching QA MySQL Server
    sh launchDB.sh $2 $3
    return_from_mysql_container_launching=$?
    if [ "$return_from_mysql_container_launching" -eq 1 ]; then 
        echo "Impossible de poursuivre le processus de release"
        echo ""
        exit 1
    fi
    if [ "$return_from_mysql_container_launching" -eq 100 -a "$3" = "--db_delta" ]; then 
        echo "Le container ayant été créé, le schéma de la base sera installé en full et non en delta comme demandé."
        echo ""
    fi
    sleep 2

    # Disponibility MySQL server vérification
    sh aliveDB.sh $2
    if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    sleep 2

    # Scheme DB deployment
    if [ "$3" = '--db_full' -o "$return_from_mysql_container_launching" -eq 100 ]; then
        sh deploy_DB_scheme.sh $2 --db_full
        if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    fi
    if [ "$3" = '--db_delta' ]; then 
        sh deploy_DB_scheme.sh $2 --db_delta
        if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    fi
    sleep 2

    # Launching API
    sh launchAPI.sh $2
    if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    sleep 2

    # Disponibility API vérification (10 retries)
    sh aliveAPI.sh 10 $2
    if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    sleep 2

    # Launching Datasets periodic collecting
    sh launchDatasetCollect.sh $2

fi


