# %%
from stravalib.client import Client
import pickle
import time
client = Client()
MY_STRAVA_CLIENT_ID, MY_STRAVA_CLIENT_SECRET = open('client.secret').read().strip().split(',')

print ('Client ID and secret read from file'.format(MY_STRAVA_CLIENT_ID) )


# %%
url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='http://127.0.0.1:5000/authorization', scope=['read_all','profile:read_all','activity:read_all','activity:write'])

url

# %%
CODE = '4381cd851def03f6a2bd50113614ac80d6d500d5'

access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, code=CODE)


# %%
with open('../access_token.pickle', 'wb') as f:
    pickle.dump(access_token, f)

with open('../access_token.pickle', 'rb') as f:
    access_token = pickle.load(f)

# %%
if time.time() > access_token['expires_at']:
    print('Token has expired, will refresh')
    refresh_response = client.refresh_access_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, refresh_token=access_token['refresh_token'])
    access_token = refresh_response
    with open('../access_token.pickle', 'wb') as f:
        pickle.dump(refresh_response, f)
    print('Refreshed token saved to file')
    client.access_token = refresh_response['access_token']
    client.refresh_token = refresh_response['refresh_token']
    client.token_expires_at = refresh_response['expires_at']
        
else:
    print('Token still valid, expires at {}'
          .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))
    client.access_token = access_token['access_token']
    client.refresh_token = access_token['refresh_token']
    client.token_expires_at = access_token['expires_at']

# %%
walk = client.get_activity(9490909968)

description = walk.description

client.update_activity(9490909968, description="")

# %%
walk = client.get_activity(9490909968)
walk.gear_id

walk.type

# %%
for activity in client.get_activities(limit=500):
    if (activity.type=="Walk"):
        # print("walk")
        client.update_activity(activity.id, gear_id='g7613511')


