#!/usr/bin/python3

import instaloader
from sightengine.client import SightengineClient

#TODO : LOg system
#TODO : UI (InstabruteForce Display)


debug = True
if debug :
    with open ('C:/Users/NP/Desktop/InstaFinderTEst.txt', 'r') as file :
        username, password, _ = file.readline().split(':')
else:
    username = input('Your Username : ')
    password = input('Your password')

instaClient = instaloader.Instaloader()
instaClient.login(username, password)
apiClient = SightengineClient('1169033501', '7ymikLMsYSdhYpjVA2xd')

class node ():
    def __init__(self, userPro, viewer, quickMode=True):
        self.quickMode = quickMode
        self.viewer = viewer
        self.qualuty = 0
        self.posts = []
        self.users = []
    
        if  type(userPro) == str :
            self.username = userPro
            self.profile = instaloader.Profile.from_username(viewer.context, userPro)
        else:
            self.username = userPro.username
            self.profile = userPro
        
        if debug : print('Node ({}) Made'.format(self.username))

    def calcFitScroe(self, gender='male', num=10, minor=0, nude=0):
        self.fitScore = 0
        inum = 0
        for post in self.profile.get_posts():

            if inum >= num : break
            output = apiClient.check('nudity','face-attributes').set_url('{}'.format(post.url))
            try :
                attr = output['faces'][0]['attributes']
            except:
                continue

            if not minor :
                ageScore = 1-attr['minor']
            else :
                ageScore = attr['minor']

            nudeAttr = output['nudity']
            if not nude :
                nudeScore = nudeAttr['safe']
            else :
                nudeScore = nudeAttr['partial']+nudeAttr['raw']
            self.fitScore += (attr[gender]+ageScore+nudeScore)/3
            inum += 1
            if debug : print('Image Score:', (attr[gender]+ageScore+nudeScore)/3)
        self.fitScore /= num
        
    def expandNode (self, option, num):
        if 'folower' in option :
            self.followers = self.profile.get_followers()
            for follower in self.followees:
                if debug :print('Expanding By Followers')
                
                if len(self.users) >= num:
                    break
                usersNode = node(follower, self.viewer, self.quickMode)
                users.append(userNode)

        if 'folowing' in option :
            self.followees = self.profile.get_followees()
            for followee in self.followees:
                if debug :print('Expanding By Followees')
                
                if len(self.users) >= num:
                    break
                usersNode = node(followee, self.viewer, self.quickMode)
                users.append(userNode)
                
        if 'tag' in option :
            for post in self.profile.get_tagged_posts():
                if debug :print('Expanding By Tag')
                
                if not self.quickMode:
                    self.posts.append(post)
                
                if len(self.users) >= num:
                    break
                for user in post.tagged_users :
                    if user != self.username :
                        userNode = node(user, self.viewer, self.quickMode)
                        self.users.append(userNode) 

        return self.users[:num]

if __name__ == "__main__":
    testNode = node('kimkardashian', instaClient)
    print(testNode.calcFitScroe(gender='female', num=4, minor=0, nude=1))
    

#TODO:
'''
1_get page posts
2_send to picture detect api
3_get folowee if is high score
'''
#TOTEST
'''
Post.location

for post in L.get_hashtag_posts('cat'):
    # post is an instance of instaloader.Post
    L.download_post(post, target='#cat')

#Profile.from_id(L.context, USERID)
#post = Post.from_shortcode(L.context, SHORTCODE)
'''
#API
'''
# if you haven't already, install the SDK with "pip install sightengine"
from sightengine.client import SightengineClient
client = SightengineClient('1169033501', '7ymikLMsYSdhYpjVA2xd')
output = client.check('nudity','celebrities','faces','scam','face-attributes').set_url('https://sightengine.com/assets/img/examples/example7.jpg')
'''
