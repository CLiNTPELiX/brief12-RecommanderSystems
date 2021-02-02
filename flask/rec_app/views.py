from flask import Flask, request, url_for, render_template, redirect
from rec_app.process import *

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    # Recover artists selection
    ap = db()
    artists = ap['name'].unique()

    return render_template('index.html', artist_names = sorted(artists[100:120]))

@app.route('/results', methods = ["POST"])
def results():
    
    r = request.form.getlist("selection")
    
    ap = db()
    ap = preprocess(ap)
    
    ratings_df = get_ratings(ap)
    user_id = ratings_df.index.values
    artists_name = ap.sort_values("artistID")["name"].unique()

    new_user = max(user_id)+1
    nuser_artist = np.zeros(len(artists_name))
    
    for i, artist in enumerate(r):
        nuser_artist[i] = ap.playCountScaled[ap["name"]==artist].mean()

    ratings_df.loc[new_user] = nuser_artist
    user_id = ratings_df.index.values
    
    ratings = ratings_df.fillna(0).values
    X = csr_matrix(ratings)
    Xcoo = X.tocoo()

    model = fit_model(X)

    artists_name = ap.sort_values("artistID")["name"].unique()
    n_users, n_items = ratings_df.shape

    idx_list = list(user_id)
    idx = idx_list.index(new_user)
    scores = model.predict(idx, np.arange(n_items))

    top_items = artists_name[np.argsort(-scores)][:10]

    reco = []
    
    for i in top_items:
        if i not in r:
            reco.append(i)
    
    return render_template('results.html', selection = reco )

@app.errorhandler(404)
def page_not_found(e):
  
    return render_template('404.html'), 404