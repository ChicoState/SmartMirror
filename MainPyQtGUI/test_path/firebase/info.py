# Import database module.
import firebase_admin
import json
from firebase_admin import db
from firebase_admin import credentials

def fetchFromDb():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./firebase/messaging-18f15-firebase-adminsdk-st2pm-ae4e8ed57e.json')
    # Initialize the app with a service account, granting admin privileges

    try:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://messaging-18f15.firebaseio.com/'
        })
    except:
        print("Error Caught")

    # Get a database reference to our posts
    ref = db.reference('posts')

    # Read the data at the posts reference (this is a blocking operation)
    data = json.dumps(ref.get())

    info = json.loads(data)

    location = list(info.items())[-1]
    return location[1]['body']