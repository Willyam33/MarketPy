#!bin/sh

# CICD Testing script

if [ "$#" -ne 1 -o "$1" != "DEV" -a "$1" != "QA" -a "$1" != "DEMO" -a "$1" != "PREPROD" ]; then 
    echo "test.sh [environment (DEV/QA/DEMO/PREPROD)]" 
else
    export MARKETPY_PATH="/home/ubuntu/MarketPy"

    echo "Début des tests fonctionnels"
    # Preparing database. Be careful, this process resets all database content and returns scheme only
    python3 $MARKETPY_PATH/$1/python_test_files/prepare_data.py 

    # Testing models management (add/remove/error cases : failed access and corrupted database) by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_models_management.py > resultats.txt

    # Testing users management (add/remove/error cases : failed access and corrupted database) by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_users_management.py >> resultats.txt

    # Testing the predictions getting process (failed access and corrupted database test cases) by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_predictions_failed_access_tests.py >> resultats.txt
  
    # Testing the informations, needed for golive decisions, getting process (failed access and corrupted database test cases)  by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_golive_decision_informations_failed_access.py >> resultats.txt

    # Testing the new ml model golive process (failed access and corrupted database test cases)  by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_doing_golive_failed_access.py >> resultats.txt

    # Testing the predictions getting process (no prediction down test cases) by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_predictions_with_no_prediction_in_database.py >> resultats.txt

    # Testing the informations, needed for golive decisions, getting process (no production model test cases)  by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_golive_decision_informations_no_production_model-0.py >> resultats.txt

    # Testing the new ml model golive process (first golive test cases)  by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_doing_golive-0.py >> resultats.txt

    # Testing the listening and collecting workflow (normal case) 
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_listening_workflow_nominal_cases.py >> resultats.txt

    # Testing the informations, needed for golive decisions, getting process (no production model test cases, but dataset analysed and first scored models)  by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_golive_decision_informations_no_production_model-1.py >> resultats.txt

    # Testing the new ml model golive process (new golive test cases)  by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_doing_golive-1.py >> resultats.txt

    # Testing the listening and collecting workflow (error cases with corrupted databases) 
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_listening_workflow_database_corruption.py >> resultats.txt

    # Testing the informations, needed for golive decisions, getting process (with existing production model to replace)  by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_golive_decision_informations_with_production_model.py >> resultats.txt

    # Testing the new ml model golive process (with existing production model to replace) by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_doing_golive-2.py >> resultats.txt

    # Testing the prediction process by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_predicting_process.py >> resultats.txt

    # Testing the predictions getting process (one prediction in the database) by API
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_predictions_with_one_prediction_in_database.py >> resultats.txt
    
    # END TO END Testing
    # New valid dataset + golive -> V1.1 + prediction and get prediction
    # New model + new valid dataset + golive -> V2.0 + prediction + get prediction
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_full.py >> resultats.txt

    # Testing several others error cases on corrupted database
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_predictions_database_corruption_tests.py >> resultats.txt
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_getting_golive_decision_informations_db_corruption.py >> resultats.txt
    python3 -m pytest --no-header --no-summary $MARKETPY_PATH/$1/python_test_files/test_api_for_doing_golive_db_corruption.py >> resultats.txt

    echo "Tests fonctionnels terminés. Résultats disponibles dans le fichier resultats.txt"

    # Removing tests files
    rm $MARKETPY_PATH/$1/raw_files/*
    rm $MARKETPY_PATH/$1/incoming_files/*
    rm $MARKETPY_PATH/$1/isolated_files/*

fi
