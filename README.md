# reddit-image-download
Downloads number of images from a subreddit. Uses requests, threading and OAuth2

# requirements

Requests, Requests.auth and wget modules

You have to create an application here: https://www.reddit.com/prefs/apps/

# configuration

Open rid.py and change these values at the top to your own values

client_id = 'yourclientid' 
client_secret = 'yourclientsecret'
username = 'redditusername'
password = 'redditpassword'

# example usage

python rim.py kateupton 200

Gets 200 links from r/kateupton, filters out anything that isn't a jpg, removes duplicates and downloads the images using 8 concurrent threads.

# note

This is a somewhat personal project to get into Python programming during easter break. I do not claim this code to be perfect and this should probably not be used as example code for ones learning python. For example it lacks most error handling and it was only half-way through that I even learned about the existence of PEP8. Use at your own risk. 

I am always open to constructive criticism though. 
