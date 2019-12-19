# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:34:34 2019

@author: Kyle D
"""

import requests
import pandas as pd
import json


artist=str(input("Please enter an artist: ")).lower()
artist_2=str(input("Please enter an artist: ")).lower()
token=str(input("Please enter access token: "))
################################ INPUT 1 ####################################
payload = {
	'artist': artist,
	'limit' : 20,
	'access_tocken' : token
}
##########################################################################

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def show_wordcloud(d, title):
    wordcloud = WordCloud(width=900,height=400, max_words=20,normalize_plurals=False,
                          background_color='white').generate_from_frequencies(d)

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    fig.suptitle(title, fontsize=20)
    fig.subplots_adjust(top=2.3)
    
    plt.imshow(wordcloud)
    return wordcloud

reqs = 'http://localhost:50000/retrieve_freq_words'
r = requests.post(url = reqs, json = payload) 
dictn = json.loads(r.text)
dataset = pd.DataFrame.from_dict(dictn['words_info'])
d = dict()
i = 0
for data in dataset.index:
    d[dataset['frequent_word'][i]] = dataset['word_count'][i]
    i += 1
cloud = show_wordcloud(d, payload['artist'])
cloud.to_file(payload['artist']+'_wordcloud.png')
dataset.set_index('frequent_word').plot.bar()
plt.savefig(payload['artist']+'_wordcount.png')
print ('WordCloud Figures Generated for {}'.format(payload['artist']))
stat_info1 = dictn['stat_info']

################################ INPUT 2 ####################################
payload1 = {
	'artist':artist_2,
	'limit' : 20,
	'access_tocken' : token
}
##########################################################################

r = requests.post(url = reqs, json = payload1) 
dictn = json.loads(r.text)
dataset = pd.DataFrame.from_dict(dictn['words_info'])
d = dict()
i = 0
for data in dataset.index:
    d[dataset['frequent_word'][i]] = dataset['word_count'][i]
    i += 1
cloud = show_wordcloud(d, payload1['artist'])
cloud.to_file(payload1['artist']+'_wordcloud.png')
dataset.set_index('frequent_word').plot.bar()
plt.savefig(payload1['artist']+'_wordcount.png')
print ('WordCloud Figures Generated for {}'.format(payload1['artist']))
stat_info2 = dictn['stat_info']

print ('Average words per song for {} : {}'.format(payload['artist'], round(stat_info1['average'])))
print ('Highest words in a song for {} : {}'.format(payload['artist'], stat_info1['max']))
print ('Lowest words in a song for {} : {}'.format(payload['artist'], stat_info1['min']))
print ('Average words per song for {} : {}'.format(payload1['artist'], round(stat_info2['average'])))
print ('Highest words in a song for {} : {}'.format(payload1['artist'], stat_info2['max']))
print ('Lowest words in a song for {} : {}'.format(payload1['artist'], stat_info2['min']))