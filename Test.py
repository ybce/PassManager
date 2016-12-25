import spotipy


spotify = spotipy.Spotify()
name = 'Radiohead'

results = spotify.artist_top_tracks('4Z8W4fKeB5YxbusRsdQVPb')
#Get data from json object
for i, item in enumerate(results['tracks']):
    print i+1, item['name']

