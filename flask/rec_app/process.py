from lightfm import LightFM
from scipy.sparse import csr_matrix

import numpy as np
import pandas as pd

def fit_model(X):
    learning_rate = 0.08
    loss = 'warp'
    k = 5
    num_threads = 4
    random_state = 42
    
    model = LightFM(learning_rate=learning_rate, k=k, learning_schedule='adadelta', loss=loss, random_state=random_state)
    model.fit(X, num_threads=num_threads)
    
    return model

def db():
    plays = pd.read_csv('~/Code/repositoryGIT/Bloc 2/brief12-RecommanderSystems/flask/rec_app/datasets/user_artists.dat', sep='\t')
    artists = pd.read_csv('~/Code/repositoryGIT/Bloc 2/brief12-RecommanderSystems/flask/rec_app/datasets/artists.dat', sep='\t', usecols=['id','name']) # id name url pictureURL

    ap = pd.merge(artists, plays, how="inner", left_on="id", right_on="artistID")
    ap = ap.rename(columns={"weight": "playCount"})
    
    artist_names = list(set(ap['name']))

    artist_rank = ap.groupby(['name']) \
        .agg({'userID' : 'count', 'playCount' : 'sum'}) \
        .rename(columns={"userID" : 'totalUsers', "playCount" : "totalPlays"}) \
        .sort_values(['totalPlays'], ascending=False)

    artist_rank['avgPlays'] = artist_rank['totalPlays'] / artist_rank['totalUsers']
    ap = ap.join(artist_rank, on="name", how="inner") \
         .sort_values(['playCount'], ascending=False)

    return ap

def preprocess(ap):
    pc = ap.playCount
    playcountscaled = (pc - pc.min()) / (pc.max() - pc.min())
    ap = ap.assign(playCountScaled=playcountscaled)
    
    return ap
    
def get_ratings(ap):
    ratings_df = ap.pivot(index='userID', columns='artistID', values='playCountScaled')
    
    return ratings_df