import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials 
from config import CLIENT_ID, CLIENT_SECRET, USERNAME

def get_data():
    cid = CLIENT_ID
    csecret = CLIENT_SECRET
    redirectURI = 'http://localhost:8888'

    #username = "contreras.andres19"
    username = USERNAME

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=csecret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    scope = 'user-read-currently-playing'

    # Takes the user to the redirectURI to authentica themselves and give the app access to their data
    token = util.prompt_for_user_token(username, scope, cid, csecret, redirectURI)

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)

    current_track = sp.current_user_playing_track()
    #print(current_track)
    #print(json.dumps(current_track, sort_keys=False, indent=4))

    if current_track is None:
        data = ""
        with open("data.json") as f: #in read mode, not in write mode, careful
            data = json.load(f)

        data['is_playing'] = False
        return (data)


    with open("data.json","w") as f: #in write mode
        json.dump(current_track,f)

    #All the Json output
    '''
    print(json.dumps(current_track, sort_keys=False, indent=4))

    print("%s" % (current_track['item']['album']['artists'][0]['name']))

    print("%s" % (current_track['item']['album']['artists'][0]['name']))
    #"name":
    print("%s" % (current_track['item']['name']))

    #"progress_ms":
    print("%s" % (current_track['progress_ms']))

    #"duration_ms":
    print("%s" % (current_track['item']['duration_ms']))

    #"is_playing":
    print("%s" % (current_track['is_playing']))

    #"images":
    print("%s" % (current_track['item']['album']['images'][0]['url']))
    '''

    return current_track
