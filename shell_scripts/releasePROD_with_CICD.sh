#!bin/sh

# Tagging GIT -> Pull Request on DEV -> Deploying QA -> Launching QA Servers (API and MySQL) -> Testing -> If OK -> GO LIVE

if [ "$#" -ne 2 -o "$2" != '--db_delta' -a "$2" != "--db_full" -a "$2" != "--no_db_update" ]
then 
    echo "releasePROD_with_CICD.sh [Version_Tag] --db_full" 
    echo "releasePROD_with_CICD.sh [Version_Tag] --db_delta"
    echo "releasePROD_with_CICD.sh [Version_Tag] --no_db_update"
else
    export MARKETPY_PATH=/home/ubuntu/MarketPy

    # Tagging GIT

    # Pull Request on DEV

    # Installation of deployment python files
    sh install_deployment_py_files.sh QA

    # Disponibility API vérification (1 retry)
    sh aliveAPI.sh 1 QA
    if [ "$?" -eq 0 ]; then 
        # Shutting down the API
        sh shutdownAPI.sh QA
    else
        echo "Pas d'API à éteindre"
        echo ""
    fi
    sleep 2

    # Shutting down Dataset Collect process if alive
    sh shutdownDatasetCollect.sh QA
    sleep 2

    # Deploying application in QA environment
    sh deploy_APP.sh QA
    if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    sleep 2

    # Launching QA MySQL Server
    sh launchDB.sh QA $2
    return_from_mysql_container_launching=$?
    if [ "$return_from_mysql_container_launching" -eq 1 ]; then 
        echo "Impossible de poursuivre le processus de release"
        echo ""
        exit 1
    fi
    if [ "$return_from_mysql_container_launching" -eq 100 -a "$2" = "--db_delta" ]; then 
        echo "Le container ayant été créé, le schéma de la base sera installé en full et non en delta comme demandé."
        echo ""
    fi
    sleep 2

    # Disponibility MySQL server vérification
    sh aliveDB.sh QA
    if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    sleep 2
 

    # Scheme DB deployment
    if [ "$2" = '--db_full' -o "$return_from_mysql_container_launching" -eq 100 ]; then
        sh deploy_DB_scheme.sh QA --db_full
        if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    fi
    if [ "$2" = '--db_delta' ]; then 
        sh deploy_DB_scheme.sh QA --db_delta
        if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    fi
    sleep 2

    # Launching API
    sh launchAPI.sh QA
    if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    sleep 2

    # Disponibility API vérification
    sh aliveAPI.sh 10 QA
    if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
    sleep 2

    # Testing
    echo "Lancement des tests de QA" 
    sh test.sh QA

    # Shutting down API
    sh shutdownAPI.sh QA
    
    # Si seulement un test est en échec, on interrompt le déploiement
    if [ $(grep " failed" resultats.txt | wc -l) -gt 0 ]; then
        echo "Des erreurs ont été trouvées. Impossible de poursuivre le processus de release. Voir le fichier resultats.txt."
        echo ""
    else
        # GO LIVE
        echo "Aucune erreur. Poursuite du déploiement en PROD"

        # Installation of deployment python files
        sh install_deployment_py_files.sh PROD
    
        # Disponibility API vérification (1 retry)
        sh aliveAPI.sh 1 PROD
        if [ "$?" -eq 0 ]; then 
            # Shutting down the API
            sh shutdownAPI.sh PROD
        fi
        sleep 2

        # Shutting down Dataset Collect process if alive
        sh shutdownDatasetCollect.sh PROD
        sleep 2

        # Deploying application in PROD environment
        sh deploy_APP.sh PROD
        if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
        sleep 2

        # Launching PROD MySQL Server
        sh launchDB.sh PROD $2 
        return_from_mysql_container_launching=$? 
        if [ "$return_from_mysql_container_launching" -eq 1 ]; then 
            echo "Impossible de poursuivre le processus de release"
            echo ""
            exit 1
        fi
        if [ "$return_from_mysql_container_launching" -eq 100 -a "$2" = "--db_delta" ]; then 
            echo "Le container ayant été créé, le schéma de la base sera installé en full et non en delta comme demandé."
            echo ""
        fi
        sleep 2

        # Disponibility MySQL server vérification
        sh aliveDB.sh PROD
        if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
        sleep 2

        # Scheme DB deployment
        if [ "$2" = '--db_full' -o "$return_from_mysql_container_launching" -eq 100 ]; then
            sh deploy_DB_scheme.sh PROD --db_full
            if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
        fi
        if [ "$2" = '--db_delta' ]; then 
            sh deploy_DB_scheme.sh PROD --db_delta
            if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
        fi
        sleep 2

        # Launching API
        sh launchAPI.sh PROD
        if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
        sleep 2

        # Disponibility API vérification
        sh aliveAPI.sh 10 PROD
        if [ "$?" -eq 1 ]; then echo "Impossible de poursuivre le processus de release"; echo ""; exit 1; fi
        sleep 2
    
        # Launching Datasets periodic collecting
        sh launchDatasetCollect.sh PROD

        echo "La version "$1" de l'application est en production ! Félicitations !!!!"
        echo ""
    fi
fi


