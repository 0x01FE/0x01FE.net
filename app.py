from flask import Flask, current_app, render_template, redirect
from os.path import exists
from math import floor
import json


app = Flask(__name__, static_url_path='', static_folder='static')


spotify_times_path = "/home/jackson/docker/volumes/spotify/jackson/"
templates_path = "~/0x01fe.net/templates/"
css_path = "~/0x01fe.net/"
assets_path = "~/0x01fe.net/assets/"





def listenTimeFormat(mili : int) -> tuple:

    minutes = mili/1000/60
    hours = floor(minutes/60)

    return (hours, round(minutes % 60))



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
    i = 0
    for artist_tuple in data:
        artist_name, artist_info = artist_tuple

        top_ten[artist_name.replace("-", " ")] =  listenTimeFormat(artist_info["overall"])
        i+=1
        if i == 10:
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

    artist = artist.lower()

    with open(spotify_times_path + "overall.json", 'r') as f:
        data = json.loads(f.read())

    listen_time = listenTimeFormat(data[artist]["overall"])

    # Make a dict of my top five albums for artist
    albums_sorted = sorted(data[artist]["albums"].items(), key=keyfunc, reverse=True)

    top_albums = {}
    i = 0
    for album_tuple in albums_sorted:
        album_name, album_info = album_tuple

        top_albums[album_name] = listenTimeFormat(album_info["overall"])
        i+=1
        if i == 5:
            break

    # Make a dict of my top ten songs for artist
    all_songs = {}
    for album in data[artist]["albums"]:
        for song in data[artist]["albums"][album]["songs"]:
            all_songs[song] = data[artist]["albums"][album]["songs"][song]

    sorted_songs = {k: v for k, v in sorted(all_songs.items(), key=lambda item: item[1], reverse=True)}

    top_songs = {}
    i = 0
    for song in sorted_songs:
        top_songs[song] = listenTimeFormat(sorted_songs[song])
        i+=1
        if i == 10:
            break

    if exists(f'./music{artist}.html'):
        return render_template(f'./music/{artist}.html', css_path=css_path, assets_path=assets_path, artist_listen_time=listen_time, top_albums=top_albums, top_songs=top_songs)
    else:
        return render_template('./music/default-artist.html', css_path=css_path, assets_path=assets_path, artist_name=artist.title() , artist_listen_time=listen_time, top_albums=top_albums, top_songs=top_songs)
