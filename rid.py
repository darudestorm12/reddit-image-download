import requests
import requests.auth
import re
import time
import json
import wget
import math
import sys
from collections import OrderedDict
import threading
from Queue import Queue

client_id = ''
client_secret = ''
username = ''
password = ''

def main():
    rd = RedditDownload(client_id, client_secret, username, password)

    if len(sys.argv) <= 2:
        sys.exit("Usage: python upton.py <subreddit> <limit>")
    
    subreddit = sys.argv[1]
    limit = sys.argv[2]    
    print "Retrieving links.."
    token = rd.getToken()
    links = rd.getLinks(subreddit, token, limit)
    cLinks = len(links)
    print "Retrieved links: ", cLinks
    print "Eliminating duplicates.."
    links = list(OrderedDict.fromkeys(links))
    print "Links left: ", len(links)
    print "Starting download.."
    print ""
    rd.tDownload(links)

class RedditDownload:
    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password


    def getToken(self):
        client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        post_data = {"grant_type": "password", "username": self.username, "password": self.password}
        headers = { "User-Agent": "rid/0.1 by rickstick19" }
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        json_dict = response.json()
        return json_dict['access_token']

    def getLinks(self, subreddit, token, limit ):
        links = []
        after = None 
        thetoken = "bearer " + token
        headers = {"Authorization": thetoken, "User-Agent": "rid/0.1 by rickstick19"}
        
        if limit > 100:
            c = math.ceil(float(limit)/100)
        else:
            c = 1   
        count = 1   
        while count <= c: 
            if count == 1:
                params = { "t":"all", "limit": limit, "show":"all"}
            else:
                params = { "t":"all", "limit": limit, "show":"all", "after":after}  
            response = requests.get("https://oauth.reddit.com/r/"+subreddit+"/top", headers=headers, stream=False, params=params)
            #print(json.dumps(response.json(), indent=4))
            json_dict = response.json()
            after = json_dict['data']['after']
            for key in json_dict['data']['children']:
                url = key['data']['url']
                if (url.lower().endswith('.jpg')) or (url.lower().endswith('.jpeg')):
                    links.append(url)
            count = count + 1
            time.sleep(1)   
        return links

    def worker(self):
        while not self.q.empty():
            item = self.q.get()
            try: 
                wget.download(item)
            except IOError, e:
                print("Something went wrong ",e)
            self.q.task_done()

    def tDownload (self, links):
        self.q = Queue()

        for item in links:
            self.q.put(item)

        for i in range(8):
            t = threading.Thread(target=self.worker)
            t.daemon = False
            t.start()

        self.q.join()

if __name__ == '__main__':
    main()
