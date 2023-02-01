import tensorflow as tf
import pandas as pd
import os
from keras.models import load_model
import matplotlib as plt
import numpy as np

def predict(model_name, headers_to_write, headers_to_drop):
    os.chdir(f'{os.getcwd()}')

    output = pd.DataFrame()

    # Load the TensorFlow model
    model = tf.keras.models.load_model(model_name)

    # Load the data into a Pandas dataframe
    #test_data/
    df = pd.read_csv('train.csv')

    if model_name == 'shad.h5':
        df_train = pd.read_csv('train_data/shad_train_xG.csv').drop(headers_to_write, axis=1)
    elif model_name == 'isaac.h5':
        df_train = pd.read_csv('train_data/isaac_train_xG.csv').drop(headers_to_write, axis=1)

    output[headers_to_write] = df[headers_to_write]

    df = df.drop(headers_to_drop, axis=1)
    df_norm = (df - df_train.mean()) / df_train.std()

    # Run the prediction
    predictions = model.predict(df_norm)
    pred_headers = ['pred_' + h for h in headers_to_write]
    output[pred_headers] = pd.DataFrame(predictions)
    #results['prediction'] = prediction
    pd.DataFrame(output).to_csv("predictions.csv", index=False, header=False)