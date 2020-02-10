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
    def __init__(self, userPro, viewer):
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

    def calcFitScroe(self, gender='male', num=10, adult=1, nude=0):
        self.fitScore = 0
        inum = 0
        
        for post in self.profile.get_posts():
            if inum >= num : break
            output = apiClient.check('nudity','face-attributes').set_url('{}'.format(post.url))
            try :
                attr = output['faces'][0]['attributes']
            except:
                print('NO FACE DETECTED')
                continue
            
            ageScore = (1*adult)+(-1*adult)* attr['minor']
            nudeScore = (1*nude)+(-1*nude)* output['nudity']['safe']
            try :
                if output['nudity']['partial_tag']:nusescore = 1
            except :
                pass
            
            imgFitScore = (attr[gender] + ageScore + nudeScore)/3
            
            self.fitScore += imgFitScore
            self.posts.append({post:[output, imgFitScore]})

            inum += 1
            if debug : print('Image Score:{} \ngender{}:{} adult{}:{} nude{}:{}\n{}\n'.format(
                imgFitScore, gender, attr[gender], adult, ageScore, nude, nudeScore, post.url))
            
        self.fitScore /= num
        return self.fitScore
        
    def expandNode (self, option, num):
        if 'folower' in option :
            self.followers = self.profile.get_followers()
            for follower in self.followees:
                if debug :print('Expanding By Followers')
                
                if len(self.users) >= num:
                    break
                usersNode = node(follower, self.viewer)
                users.append(userNode)

        if 'folowing' in option :
            self.followees = self.profile.get_followees()
            for followee in self.followees:
                if debug :print('Expanding By Followees')
                
                if len(self.users) >= num:
                    break
                usersNode = node(followee, self.viewer)
                users.append(userNode)
                
        if 'tag' in option :
            for post in self.profile.get_tagged_posts():
                if debug :print('Expanding By Tag')
                
                self.posts.append(post)
                
                if len(self.users) >= num:
                    break
                for user in post.tagged_users :
                    if user != self.username :
                        userNode = node(user, self.viewer)
                        self.users.append(userNode) 

        return self.users[:num]

if __name__ == "__main__":
    testNode = node('kimkardashian', instaClient)
    fitScore = testNode.calcFitScroe(gender='female', num=4, adult=1, nude=1)
    if fitScore >= 0.45:
        testNode.expandNode('tag folowing', 10)
    

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
