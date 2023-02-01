# Rocket League Predictor
Predicts likelihood of winning a Rocket League game from game statistics - see if you are unlucky or lucky!

Tensorflow prediction model to assess team performance in a game.

Only works on 2v2 games currently and some player ID data is hardcoded in the create_frames.py file - this is to filter out unwanted replays.

Uses statistics from ballchasing.com, such as:
- shots for/against
- % in zones (halves, thirds) for/against
- bpm for/against
- boost for/against
- demos for/against

'main.py' - takes a URL from ballchasing.com and downloads all replays on the page currently displayed. Make sure to delete all files from the 'csvs' folder before using this otherwise they will not be saved!
    
'create_frames.py' - merges and filters all replay statistic files creating 'combined_data.csv', 'filtered_data.csv', 'raw_train.csv' and 'train.csv'. Only 'train.csv' is of interest. This contains all feature points + the goals scored/conceded (for training/validation).
      
'/xG_model/model.py' - this is the Tensorflow training model and create the model for predictions.

The model architecture:

![Model Architecture](https://github.com/isaactallack/RL-xG-Predictor/blob/main/images/isaac.h5.svg?raw=true)
   
'poisson.py' is used to model the scoring of goals as a Poisson distribution when the distribution is centered around the xG or each team. Then by comparing the probabilities of scoring x goals at each point you can calculate the probability that a team won the game. An example of what this might look like if team A had an xG or 2.8 and team B had an xG of 0.6:

![Model Architecture](https://github.com/isaactallack/RL-xG-Predictor/blob/main/images/poisson.png?raw=true)

In this case, team A has a 89% chance of winning the game. 

'predict.py' - use this to predict the results from 'train.csv'.
