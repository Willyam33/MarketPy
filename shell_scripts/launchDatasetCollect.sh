#!bin/sh

if [ "$#" -ne 1 -o "$1" != "DEV" -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" -a "$1" != "PROD" ]; then 
    echo "launch.sh [environment (DEV/QA/DEMO/PREPROD/PROD)]" 
    exit 1
else
    # Launching Datasets periodic collecting
    export MARKETPY_PATH=/home/ubuntu/MarketPy
    python3 $MARKETPY_PATH/$1/python_files/dataset_collect_main.py &
    exit 0
fi




