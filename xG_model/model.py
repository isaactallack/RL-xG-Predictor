import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import numpy as np

os.chdir(f'{os.getcwd()}')

# Load the data
data = pd.read_csv('train.csv')

features = data.drop(['goals-a', 'goals conceded-a'], axis=1)
#results = data[['result', 'gd']]
results = data[['goals-a', 'goals conceded-a']]
#gd = data['gd']

tf.random.set_seed(1)
norm_feat = (features - features.mean()) / features.std()

##############################################

#'''
# Split the data into training and test sets
train_data, test_data, train_results, test_results = train_test_split(norm_feat, results, test_size=0.25, random_state = 1)

# Create the neural network
# Build the model
model = tf.keras.Sequential([
  tf.keras.layers.Dense(64, activation='relu', input_shape=(110,)),
  tf.keras.layers.Dense(32, activation='relu'),
  tf.keras.layers.Dense(2)
])

# Compile the model
#model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Compile the model
model.compile(optimizer='adam',
              loss=tf.losses.MeanSquaredError(),
              metrics=['mae'])

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_mae', patience=10, restore_best_weights=True)

# Train the model on the training data
history = model.fit(train_data, train_results, epochs=10000, batch_size = 1, callbacks = [early_stopping], validation_data=(test_data, test_results)) #verbose=0)

# Create subplots for loss and accuracy
fig, (ax1, ax2) = plt.subplots(1, 2)

# Plot the loss over time
ax1.plot(history.history['loss'])
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')

# Plot the accuracy over time
ax2.plot(history.history['mae'])
ax2.set_xlabel('Epoch')
ax2.set_ylabel('MAE')

# Show the plots
plt.show()

# Evaluate the model on the test data
score = model.evaluate(test_data, test_results, verbose=0)
print(score)

# Save the trained model
model.save('xG_model.h5')
#'''
