from flask import Flask, current_app, render_template, redirect
from operator import itemgetter
import json


app = Flask(__name__, static_url_path='', static_folder='static')


spotify_times_path = "/home/jackson/docker/volumes/spotify/jackson/data/"
templates_path = "~/0x01fe.net/templates/"
css_path = "~/0x01fe.net/"
assets_path = "~/0x01fe.net/assets/"



def keyfunc(tup :  tuple):
    key, d = tup
    return d['overall']



@app.route('/')
def root():
    return redirect('/index')



@app.route('/index')
def index():
    return render_template('index.html', css_path=css_path, assets_path=assets_path)



@app.route('/uses')
def uses():
    return render_template('uses.html', css_path=css_path, assets_path=assets_path)



@app.route('/media')
def media():

    with open(spotify_times_path + "overall.json", 'r') as f:
        data = json.loads(f.read())

    data = sorted(data.items(), key=keyfunc, reverse=True)

    top_ten = {}
    i = 1
    for artist_tuple in data:
        artist_name, artist_info = artist_tuple
        top_ten[artist_name] = {}
        top_ten[artist_name]["overall"] = round(artist_info["overall"]/1000/60/60, 1) # miliseconds to hours
        top_ten[artist_name]["place"] = i
        i+=1

    print(top_ten)

    return render_template('media.html', css_path=css_path, assets_path=assets_path, data=top_ten)



@app.route('/about')
def about():
    return render_template('about.html', css_path=css_path, assets_path=assets_path)



@app.route('/contact')
def contact():
    return render_template('contact.html', css_path=css_path, assets_path=assets_path)
