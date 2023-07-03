from flask import Flask, current_app, render_template, redirect
import json


app = Flask(__name__, static_url_path='', static_folder='static')


spotify_times_path = "/home/jackson/docker/volumes/spotify/jackson/"
templates_path = "~/0x01fe.net/templates/"
css_path = "~/0x01fe.net/"
assets_path = "~/0x01fe.net/assets/"





def militohours(mili : int) -> int:
    return mili/1000/60/60


def keyfunc(tup :  tuple) -> int:
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
        top_ten[artist_name.replace("-", " ")] = round(militohours(artist_info["overall"]), 1) # miliseconds to hours
        i+=1
        if i == 11:
            break

    return render_template('media.html', css_path=css_path, assets_path=assets_path, data=top_ten)



@app.route('/about')
def about():
    return render_template('about.html', css_path=css_path, assets_path=assets_path)



@app.route('/contact')
def contact():
    return render_template('contact.html', css_path=css_path, assets_path=assets_path)


@app.route('/music/<artist>')
def music(artist : str):

    with open(spotify_times_path + "overall.json", 'r') as f:
        data = json.loads(f.read())

    artist_listen_time = round(militohours(data[artist]["overall"]), 1)

    return render_template(f'./music/{artist}.html', css_path=css_path, assets_path=assets_path, artist_listen_time=artist_listen_time)
