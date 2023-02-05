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

    echo "Lancement de l'API sur l'environnement de "$1" sur le port "$PORT
    export MARKETPY_PATH=/home/ubuntu/MarketPy
    python3 $MARKETPY_PATH/$1/python_files/api_main.py &
    exit 0
fi
