# MarketPy

Objet

Créer et mettre à disposition un dispositif de détermination du prix d’une location saisonnière en fonction de ses caractéristiques intrinsèques, de sa localisation, de la période de location et du temps avant cette période de location.
Pour ce faire le logiciel s’appuiera sur des algorithmes de machine learning et plus précisément de régression.

Simplification :

La composante de temps : location à plusieurs périodes données devrait nécessiter la maintenance en production de plusieurs modèles. Seul un modèle pour une période précise sera mis à disposition.
L’entrainement se fera sur un ensemble de villes côtières de l’arc méditerranéen.La dimension localisation (département), distance à la mer, voire la ville précise de la location permettraient d’améliorer nettement la précision du modèle. Ce travail n’a pas été réalisé. Par ailleurs, la vétusté ou la qualité des prestations est difficile à évaluer sur des critères objectifs. Ces aspects ne favorisent pas la prédictibilité.

Techniquement :

Le modèle doit être déployable et exploitable selon les concepts MLOPs. Capacité à piloter l’évolution du modèle selon l’évolution du contexte, à automatiser les processus de développement, d’entraînement, de déploiement (concept CICD), et à mettre à disposition les services d’utilisation / prédiction et d’administration au travers d’API sécurisées.

Les dossiers :
- shell_scripts : l'ensemble des scripts de déploiement façon CICD
- config : des fichiers de propriétés décrivant les spécificités de chaque environnement (IP fixe de la base MySQL , port de communication de l'API,... différent selon l'environnement)
- DEV : l'ensemble de l'application
  - python_files : le code source
  - python_util_files : des fichiers utiles au développeur
  - python_test files : la base de tests d'intégration et tests fonctionnels lançés automatiquement par le script shell : shell_scripts/test.sh
  - python_deploy_files : des fichiers utilisés par la chaîne de déploiement
  - test_files : jeu de données (dataset) utilisés dans le cadre des tests
  - incoming_files : dossier de réception des datasets
  - raw_files : dossier de sélection des datasets à analyser
  - isolated_files : dossier d'isolement des datasets écartés en première instance
  - model : dossier de stockage du model de ML enregistré par l'application

Les scripts de déploiement créent des répertoires à la racine pour chaque environnement (QA/PREPROD/PROD/DEMO) à l'image du répertoire de dev.
