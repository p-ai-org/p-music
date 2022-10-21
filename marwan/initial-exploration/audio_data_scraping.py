'''
This file will include exploration of pulling song data from the fma repository, the goal
is to take a bunch of albums and there lists of songs and explore how we can extract song data from that.
'''

#Initial Exploration of FMA dataset


'''
Experimenting with API pulls from Spotify and Youtube
I will be experimenting using the SPOTIPY API!
This is just the template demo code given in the example for the SPOTIPY API documentation


Before running make sure to set environment variables
SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
so that Spotipy knows how/what to do when running your project.

Now let's experiment with some spotify stuff!!

'''
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
#Let's create a dictionary of artist ID"s we want to search
artist_id_dict = {}

results = sp.current_user_saved_tracks()
#iterate through the top saved tracks in the users dict
for idx, item in enumerate(results['items']):
    track = item['track']
    artist_name = track['artists'][0]['name']
    artist_uri = track['artists'][0]['uri']
    artist_id_dict[artist_name] = artist_uri
    
#now we have a list of artist dicts we can access


#Now let's try doing some searches for these artists, let's say 
#we want to find out alot about 'Kanye West'
kanye_west_id = artist_id_dict['Kanye West']
kanye_west_albums = sp.artist_albums(kanye_west_id, limit=20)


#loop through kanye albums and find things
kanye_west_albums = kanye_west_albums['items']

#print the album keys
first_album = kanye_west_albums[0]
print(first_album.keys())
print(first_album['external_urls']['spotify'])

#try getting the album previews :)

for album in kanye_west_albums:
    print(
        album['name'], ' has ', album['total_tracks'], 'tracks.',
        )

#now let's get the album url to use spotdl