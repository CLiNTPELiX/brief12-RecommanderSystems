from lightfm import LightFM
from scipy.sparse import csr_matrix

import numpy as np
import pandas as pd

def db():
    plays = pd.read_csv('~/Code/repositoryGIT/Bloc 2/brief12-RecommanderSystems/flask/rec_app/datasets/user_artists.dat', sep='\t')
    artists = pd.read_csv('~/Code/repositoryGIT/Bloc 2/brief12-RecommanderSystems/flask/rec_app/datasets/artists.dat', sep='\t', usecols=['id','name']) # id name url pictureURL

    ap = pd.merge(artists, plays, how="inner", left_on="id", right_on="artistID")
    ap = ap.rename(columns={"weight": "playCount"})
    
    artist_names = list(set(ap['name']))
    return artist_names

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
    play_count_scaled = (pc - pc.min()) / (pc.max() - pc.min())
    ap = ap.assign(playCountScaled=play_count_scaled)
    
    return ap
    
def get_ratings(ap):
    ratings_df = ap.pivot(index='userID', columns='artistID', values='playCountScaled')
    
    return ratings_df

def get_Xcoo(ratings_df):
    ratings = ratings_df.fillna(0).values  
    X = csr_matrix(ratings)
    Xcoo = X.tocoo()
    
    return Xcoo

def fit_model(X):
    learn_rate = 0.05
    nb_epochs = 25
    k = 10
    loss = 'warp-kos'
    nb_comp = 20
    model = LightFM(learning_rate=learn_rate, k=k, loss=loss, 
                 random_state = 42, no_components=nb_comp)
    model.fit(X, epochs=nb_epochs, num_threads=2)
    
    return model

def get_recommandation(userID, model, user_ids, ap, n_reco=10):
    artist_names = ap.sort_values("artistID")["name"].unique()
    ratings_df = get_ratings(ap)
    n_users, n_items = ratings_df.shape
    liste_user_idx = list(user_ids)
    idx = liste_user_idx.index(userID)
    scores = model.predict(idx, np.arange(n_items))
    top_items_pred = artist_names[np.argsort(-scores)]
    
    return top_items_pred

