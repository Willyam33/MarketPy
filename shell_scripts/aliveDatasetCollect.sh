#!bin/sh

if [ "$#" -ne 1 -o "$1" != "DEV" -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" -a "$1" != "PROD" ]; then 
    echo "aliveDatasetCollect.sh [environment (DEV/QA/DEMO/PREPROD/PROD)]" 
    exit 1
else
    PATH_TO_KILL=$1/python_files/dataset_collect_main.py
    nbline=`ps -ef | grep $PATH_TO_KILL | wc -l`
    while [ $nbline -gt 1 ]
    do
        LINE=`ps -ef | grep $PATH_TO_KILL | head -n 1`
        PROCESS_TO_KILL=`ps -ef | grep $PATH_TO_KILL | head -n 1 | tr -s " " | cut -d " " -f 2`
        PYTHON3=
        kill -9 $PROCESS_TO_KILL
        nbline=`ps -ef | grep $PATH_TO_KILL | wc -l`
        if [ "$nbline" -le 1 ]; then exit 0; fi
        sleep 5

    done
fi




