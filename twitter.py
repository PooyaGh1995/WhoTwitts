import tweepy
from tweepy import OAuthHandler
import arabic_reshaper
from bidi.algorithm import get_display
import time
import argparse
import string
#import config
import json

from tweepy import Stream
from tweepy.streaming import StreamListener


consumer_key='VnVDUqTccrmC0uFsPIyPpgj2P'
consumer_secret='cA2i6wIAsDDbWfyuEJEMEcUsbwjLlYNIQS0gb3gyRE8ulkw1iN'
access_token='2813884716-ra4CTJ1Emu6DsECRJl25WUL66q9mxffFG8R9suf'
access_secret='CzXYbtVp6rlFBX3azUAlYZPGyUyb4RROjwl81jwS6d2h8'
auth=OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api=tweepy.API(auth)
#twitter_stream = Stream(auth, MyListener())
#twitter_stream.filter(track=['#python'])
f_rouhani=open('Rouhani_Twitts.txt','w')
f_about_rouhani=open('Twitts_About_Rouhani.txt','w')

for tweet in tweepy.Cursor(api.search,
                           q='#روحانی',
                           since='2018-4-6',
                           until='2018-4-10',
                           geocode='35.6891980,51.3889740,2000km',
                           lang='fa').items(200):
    #print('Tweet by: @' + tweet.user.screen_name)
    #t=get_display(arabic_reshaper.reshape(tweet.text))
    #print('Tweet text: ' + t)
    f_rouhani.write("%s\n" % tweet.text)

for status in tweepy.Cursor(api.user_timeline, id="Rouhani_ir").items(15):
        #tt=get_display(arabic_reshaper.reshape(status.text))
        #print('Rouhani Tweet text: ' + tt)
        f_about_rouhani.write("%s\n" % status.text)

#for status in tweepy.Cursor(api.home_timeline).items(10):
#    t=get_display(arabic_reshaper.reshape(status.text))
#    print(t)
