# Centralized all data processing like preprocessing, machine learning, ...

import requests
import numpy as np
import os
import datetime
from time import strftime
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from importlib import import_module

from joblib import dump
import json
import properties

def get_dataframe_from_file(filename:str,filepath=properties.raw_files_folder):
    ''' Opening file and getting dataframe
        Parameters :
            File name
            File path
        Returns :
            Dataframe 
    '''
    return pd.read_csv(filepath+filename)

def clean_data(df):
    ''' Cleaning received dataframe
        Parameters :
            Dataframe
        Returns :
            Dataframe 
    '''
    try:
        dfc = df.drop_duplicates()
        dfc = dfc.drop(['house_type','city_name','comments_nb'],axis=1)
        dfc = dfc[dfc['rating']!="Pas de note"]
        dfc = dfc[dfc['rating']!="Nouveau"]
        dfc = dfc[dfc['rating']!="Superhôte"]
        dfc = dfc[dfc['price_week']<8000]
        dfc = dfc[dfc['bathroom']!='Demi-salle']
        dfc = dfc[dfc['bathroom']!='5,5']
        dfc['rating'] = pd.to_numeric(dfc['rating'])
        dfc['bathroom'] = pd.to_numeric(dfc['bathroom'])
        dfc = dfc.dropna()
        dfc[['jacuzzi', 'pool']]=dfc[['jacuzzi', 'pool']].astype(int)
        return dfc
    except :
        return pd.DataFrame()

def prepare_features(df):
    ''' Preparing features used for training 
        Parameters :
            Dataframe 
        Returns
            Dataframe
    '''
    # Numeric variables
    num=df[['rating','bedroom','bathroom','nb_equip']]
    # Categorical variables -> Dichotomy
    cat=df[['pool','tag','jacuzzi']]
    cat[['pool','jacuzzi']]=cat[['pool','jacuzzi']].astype(int).astype(str)
    for i,column in enumerate(cat.columns):
        if i==0:
            cat_dicho=pd.get_dummies(data=cat[column],prefix=column)
        else:
            cat_dicho=cat_dicho.join(pd.get_dummies(data=cat[column],prefix=column))
    # Joining numeric and categorical dataframe after dichotomy
    features=pd.concat([num,cat_dicho],axis=1)
    return features
    
def prepare_for_training(df):
    ''' Separating Features and Target
        Parameters : 
            Dataframe
        Returns :
            2 dataframes
    '''
    target=df['price_week']
    features=prepare_features(df)

    return features,target

def scaler_transformation(X):
    ''' Scaler transformation
        Parameters :
            Dataframe
        Returns
            Dataframe
    '''
    X[X.columns] = pd.DataFrame(StandardScaler().fit_transform(X),index=X.index)
    return X

def get_model_instance_from_module_and_name (module_name,model_name):
    ''' Getting model instance with library name and model name
        Parameters
            Library name
            Model name
        Returns
            status OK/KO
            model instance if status OK, else None
    '''
    try:
        module=import_module(module_name)
        model = getattr(module,model_name)
        return 'OK', model()
    except:
        return 'KO', None

def compute_model_score(model, X, y):
    ''' Training et evaluate model score by cross validation
        Parameters
            Model represented by library name and model name
            Features
            Target
        Returns
            Status OK / KO
            Model Score
    '''
    # Getting model object
    status, model_instance = get_model_instance_from_module_and_name (model['library'],model['name'])
    if status=='KO':    
        return 'MODEL_INSTANCE_KO', 0

    # Compute score
    cross_validation = cross_val_score(model_instance, X, y, cv=3, scoring='neg_mean_absolute_percentage_error')
    model_score = cross_validation.mean()
    return 'OK', model_score

def predict(pipeline,X):
    ''' Predicting with pipeline and features
        Parameters
            Pipeline (object)
            Feature(s)
        Returns
            Value - Prediction for price_week
    '''        
    return pipeline.predict(X)

def predict_and_score_pipeline(pipeline,X,y):
    # Predicting on test set
    ''' Predicting with pipeline and scoring
        Parameters
            Pipeline,
            Features,
            Target
        Returns
            Score value
    '''
    y_pred=predict(pipeline,X)

    # Scoring
    score = mean_absolute_percentage_error(y_pred,y).mean()
    return score

def train_and_score_model(model_library, model_name, features, target):
    ''' Training and scoring new model
        Parameters :
            Library name
            Model name
            Features
            Target
        Returns
            Model score
    '''
    status, model_instance = get_model_instance_from_module_and_name (model_library, model_name)
    if status=='KO':    
        return 'MODEL_INSTANCE_KO', None, 0

    try:
        pipeline = Pipeline(steps = [('scaler', StandardScaler()),
                                     ('model', model_instance)])

        # Separating train set and test set
        X_train, X_test, y_train, y_test = train_test_split(features,target,train_size=0.7,random_state=42)
    
        # Training on train set
        pipeline.fit(X_train, y_train)

        # Predicting then scoring
        score = predict_and_score_pipeline(pipeline,X_test,y_test)

        return 'OK', pipeline, score
    except:
        return 'TRAINING_FAILED', None, 0

    

