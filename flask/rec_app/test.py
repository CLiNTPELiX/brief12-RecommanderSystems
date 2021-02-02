from flask import Flask, render_template , request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    artists = pd.read_csv('', sep='\t', usecols=['name'])
    listed = tuple(artists['name'])[:50]
    return render_template('index.html', listed = listed)
# =============================================================================
# (@app.route('/page1')
# def page1():
#     return render_template('templates/page1'))
# =============================================================================

# =============================================================================
# @app.route('/page2')
# def page2():
#     return render_template('templates/page2')
# 
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('templates/404')
# =============================================================================
                           
if __name__ == '__main__':
    app.run(debug=True)
    
