from flask import Flask, request, url_for, render_template, redirect
from rec_app.process import *
#from rec_app.forms import artistsearchform

# ap = db ()
# ap = preprocess(ap)
# artistNames= ap.sort_values("artistID")["name"].unique()

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    artist_names = db()
    
    return render_template('index.html', artist_names = sorted(artist_names[100:110]))

@app.route('/results', methods = ["POST"])
def results():
  if request.method == "POST":
      r = request.form.getlist("selection")
  
  return render_template('results.html', selection = r)

@app.errorhandler(404)
def page_not_found(e):
  
    return render_template('404.html'), 404