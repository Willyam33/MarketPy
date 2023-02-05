#!bin/sh

if [ "$#" -ne 2 -o "$2" != "--db_full" -a "$2" != "--db_delta" -o "$1" != "DEV" -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" -a "$1" != "PROD" ]; then 
    echo "launch.sh [environment (DEV/QA/DEMO/PREPROD/PROD)] [--db_full/--db_delta]" 
    exit 1
else
    if [ $1 = "DEV" ]; then
        MYSQL_IP="172.20.0.5"
        PUBLISH="6603"
    else 
        if [ $1 = "QA" ]; then
            MYSQL_IP="172.20.0.6"
            PUBLISH="6604"
        else 
            if [ $1 = "DEMO" ]; then
                MYSQL_IP="172.20.0.7"
                PUBLISH="6605"
            else
                if [ $1 = "PREPROD" ]; then
                    MYSQL_IP="172.20.0.8"
                    PUBLISH="6606"
                else
                    if [ $1 = "PROD" ]; then
                        MYSQL_IP="172.20.0.9"
                        PUBLISH="6607"
                    fi
                fi
            fi
        fi
    fi    

    export MARKETPY_PATH="/home/ubuntu/MarketPy"
    cd $MARKETPY_PATH/$1/python_files

    cd $MARKETPY_PATH/shell_scripts

    echo "Démarrage du container MySQL sur l'environnement de "$1" - IP "$MYSQL_IP" si celui-ci n'est pas déjà démarré"
    docker container start mysql_$1
    if [ "$?" != 0 ]; then
        echo "Le container n'existe pas. (Re)création du container."
        docker run \
        --detach \
        --name=mysql_$1 \
        --env="MYSQL_ROOT_PASSWORD=msq3!xAk3c" \
        --net customnetwork \
        --ip $MYSQL_IP \
        --publish $PUBLISH:3306 \
        --volume=/root/docker/mysql_$1/conf.d:/etc/mysql/conf.d \
        mysql
        if [ "$?" -eq 0 ]; then
            echo "Le container a été recréé. Démarrage en cours."
            echo ""
            exit 100
        else
            echo "Impossible de recréer le container."
            echo ""
            exit 1
        fi
    else
        echo "Le container est démarré."
        echo ""
        exit 0
    fi
fi
