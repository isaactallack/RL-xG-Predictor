import tensorflow as tf
import pandas as pd
import os
from keras.models import load_model
import matplotlib as plt
import numpy as np

def predict(model):
    os.chdir(f'{os.getcwd()}')

    output = pd.DataFrame()

    # Load the TensorFlow model
    model = tf.keras.models.load_model(model)

    # Load the data into a Pandas dataframe
    #test_data/
    df = pd.read_csv('train.csv')

    if model == 'shad.h5':
        df_train = pd.read_csv('train_data/shad_train.csv').drop(['goals-a', 'goals conceded-a'], axis=1)
    else:
        df_train = pd.read_csv('train.csv').drop(['goals-a', 'goals conceded-a'], axis=1)

    output['goals-a'] = df['goals-a']
    output['goals conceded-a'] = df['goals conceded-a']

    df = df.drop(['goals-a', 'goals conceded-a'], axis=1)
    df_norm = (df - df_train.mean()) / df_train.std()

    # Run the prediction
    predictions = model.predict(df_norm)
    #print(predictions)
    output[['goals_pred', 'goals conceded_pred]']] = pd.DataFrame(predictions)

    #results['prediction'] = prediction
    pd.DataFrame(output).to_csv("predictions.csv", index=False, header=False)

predict('xG_model.h5')