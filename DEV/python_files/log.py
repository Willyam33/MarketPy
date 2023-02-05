# All messages and status code used in the application MarketPy

error_messages = {
    'NOT_IN_RANGE': "Au moins un paramètre n est pas dans une fourchette acceptable !", 
    'MODEL_NOT_FOUND': "Le modèle n est pas disponible, contactez votre administrateur !",
    'NO_MODEL_IN_PRODUCTION': "Pas de modèle disponible en production !",
    'USER_UNKNOWN': "L utilisateur n existe pas !",
    'NOT_ADMIN': "L utilisateur n est pas administrateur !",
    'BAD_PASSWORD': "Le mot de passe est incorrect !",
    'ERREUR_A_DEFINIR': "ERREUR A DEFINIR !",
    'USER_ALREADY_EXISTS' : " existe déjà !", # to prefix by user
    'MODEL_ALREADY_IN_BASE' : " est déjà enregistré et disponible en base !", # to prefix by model
    'MODEL_UNKNOWN' : " n existe pas en base !",
    'DATABASE_ERROR' : "Erreur d accès à la base de données",
    'DATABASE_SELECT_ERROR' : "Erreur d accès en select à la base de données",
    'DATABASE_CREATION_ERROR' : "Erreur de création de la base de données",
    'DATABASE_DROP_ERROR' : "Erreur de suppression de la base de données",
    'DATABASE_INSERT_ERROR' : "Erreur d'insertion en base de données",
    'DATABASE_UPDATE_ERROR' : "Erreur de mise à jour base de données",
    'DATABASE_DELETE_ERROR' : "Erreur de suppression dans la base de données",
    'DATABASE_INCONSISTENCY' : "Base de données inconsistante",
    'UNABLE_TO_MANAGE_PRODUCTION_MODELS' : "Impossible de gérer le modèle de production",
    'UNABLE_TO_SAVE_DATASET_METADATA' : "Impossible de sauvegarder les metadonnées du dataset. L ingestion peut être relancée manuellement ou automatiquement à la prochaine itération programmée.",
    'UNABLE_TO_LOAD_PRODUCTION_PIPELINE_FILE' : "Impossible de charger le fichier contenant le pipeline de production",
    'UNABLE_TO_SAVE_PRODUCTION_SCORING_ON_NEW_DATASET' : "Impossible de sauvegarder le score du modèle de production sur un nouveau dataset",
    'UNABLE_TO_DELETE_USER': " ne peut être supprimé !", # to prefix by user
    'UNABLE_TO_DELETE_MODEL': " ne peut être supprimé !", # to prefix by model
    'UNABLE_TO_ADD_USER': " ne peut être ajouté.e !", # to prefix by user
    'UNABLE_TO_ADD_MODEL': " ne peut être ajouté !", # to prefix by user
    'UNABLE_TO_GET_MODELS_FOR_TRAINING_AND_SCORING': "Impossible de récupérer les modèles en vue de les entrainer !", 
    'UNABLE_TO_SAVE_SCORING_IN_DATABASE': "Impossible de sauvegarder le scoring en base",
    'NO_RESULT' : "Aucun résultat",
    'FILE_SYSTEM_TROUBLE_IN_LOOKING_FOR_NEW_DATASETS' : "Problèmes rencontrés pour rechercher les fichiers contenant les datasets. L écoute est interrompue en attendant résolution du problème et relance.", 
    'FILE_SYSTEM_TROUBLE_IN_DISPATCHING_DATASETS_FILES' : "Problèmes rencontrés pour trier les fichiers contenant les datasets. L écoute est interrompue en attendant résolution du problème et relance." ,
    'MODEL_INSTANCE_KO' : "Impossible de recréer une instance du modèle à partir du nom de la librairie et du nom du modèle !",
    'TRAINING_FAILED' : "Echec de l'entraînement"
}

warning_messages = {
    'NO_MODEL_IN_PRODUCTION': "Pas de modele disponible en production !",
    'NO_PREDICTION_FOR_USER': "Aucune prédiction n a été trouvée (et probablement aucune n a été effectuée) pour ", # to suffix by user
    'NO_PREDICTION': "Aucune prédiction n a été trouvée (et probablement aucune n a été effectuée) !",
    'NO_MODEL_AVAILABLE_FOR_TRAINING_AND_SCORING': "Aucun modèle n'est disponible pour effectuer un entraînement. Contactez l'administrateur !",
    'INVALID_DATASET' : "Le dataset est invalide. Aucun entrainement, ni aucun scoring ne pourra être effectué sur celui-ci !",
    'NO_VALID_DATASET_AVAILABLE' : "Aucun dataset n est valide !",
    'NO_SCORED_MODEL_FOR_THE_LAST_VALID_DATASET' : "Pas de modèle évalué pour le dernier dataset valide !"
}

success_messages = {
    'NEW_INCOMING_FILE_FOUND': "Un nouvau dataset est disponible et peut être nettoyé et analysé !",
    'DATASET_OK': "Le nouveau dataset est nettoyé et prêt à être utilisé !",
    'NEW_MODEL_IN_PRODUCTION': "Un nouveau modèle est disponible en production !",
    'PRODUCTION_SCORING_UPDATED': "Le score du modèle de production a été mis à jour sur la base du nouveau dataset !",
    'MODEL_SCORING_FOR_NEW_DATASET_RECORDED': "Les scores des modèles ont bien été enregistrés pour le nouveau dataset !",
    'BEST_MODEL_IS': "Le meilleur modèle pour ce dataset est le modèle ",
    'USER_DELETED' : " a été supprimé.e !", # to prefix by user
    'MODEL_DELETED' : " a été supprimé !", # to prefix by user
    'USER_ADDED' : " a été ajouté.e !", # to prefix by user
    'MODEL_ADDED' : " a été ajouté !" # to prefix by user
}

informations_messages = {
    'LISTENING': "Vérification de l'arrivée évenutelle d un nouveau dataset à ", # to suffix by datetime
    'NEXT_LISTENING_IN': "Prochaine écoute dans (secondes)", # to suffix by period_listening
    'API_LAUNCH': "Lancement de l'API", 
    'API_SHUTDOWN': "Exctinction de l'API", 
    'DATASET_COLLECT_LAUNCH': "Lancement de la récupération périodique des datasts !"
}

def information(message:str,more=""):
    print("-----------------------------")
    print(informations_messages[message]+more)
    print()

def warning(message:str,more=""):
    print("--------WARNING--------------")
    print(warning_messages[message]+more)
    print()

def error(message:str,more=""):
    print("--------ERROR----------------")
    print(error_messages[message]+more)
    print()

def success(message:str,more=""):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(success_messages[message]+more)
    print()

 