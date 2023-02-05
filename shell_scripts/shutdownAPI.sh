 #!bin/sh

if [ "$#" -ne 1 -o "$1" != "DEV" -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" -a "$1" != "PROD" ]; then 
    echo "launch.sh [environment (DEV/QA/DEMO/PREPROD/PROD)]" 
    exit 1
else
    if [ $1 = "DEV" ]; then
        PORT="8000"
    else 
        if [ $1 = "QA" ]; then
            PORT="8001"
        else 
            if [ $1 = "DEMO" ]; then
                PORT="8002"
            else
                if [ $1 = "PREPROD" ]; then
                    PORT="8003"
                else
                    if [ $1 = "PROD" ]; then
                        PORT="8004"
                    fi
                fi
            fi
        fi
    fi    

    echo "Extinction de l'API sur l'environnement de "$1" sur le port "$PORT
    curl -X 'GET' -i 'http://127.0.0.1:'$PORT'/shutdown_async' -H 'username: admin' -H 'password: admin'
    #TODO : Récupérer le retour
    sleep 2
    echo "API éteinte !"
    echo ""
    exit 0

fi
