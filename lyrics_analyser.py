# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:34:34 2019

@author: Kyle D
"""

# importing the requests library
from flask import Flask, request, jsonify
import traceback
import requests 
import pandas as pd 
import re 
import nltk 
from statistics import mean
nltk.download('stopwords') 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

# API definition
app = Flask(__name__)

stopWords = stopwords.words('english')

@app.route('/retrieve_freq_words', methods=['POST'])
def retrieve_most_words():
    try:
        payload = request.json
        artist_name = payload['artist']
        limit = payload['limit']
        access_tocken = payload['access_tocken']
        header = {'Authorization': 'Bearer {}'.format(access_tocken)}
        artist = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(str(artist_name))
        r1 = requests.get(url = artist, headers=header) 
        data1 = r1.json()
        artist_id = data1['artists']['items'][0]['id']
        artist_name_get = data1['artists']['items'][0]['name']
        tracks = "https://api.spotify.com/v1/artists/{}/top-tracks?country=ES".format(artist_id)
        r = requests.get(url = tracks, headers=header) 
        data = r.json()
        
        title = []
        i = 0
        for info in data['tracks']:
            title.append(data['tracks'][i]['name'])
            i += 1
        
        lyrics_all = []
        for names in title:    
            lyrics = 'https://api.lyrics.ovh/v1/{}/{}'.format(artist_name_get, names)
            r3 = requests.get(url = lyrics) 
            data3 = r3.json() 
            try:
                lyrics_all.append(data3['lyrics'].lower())
            except:
                continue
        
        dataset_main = pd.DataFrame(lyrics_all)
        dataset_main.columns = ['lyrics']
        a = []
        for data in dataset_main['lyrics']:
            a.append(len(data.split()))
        min_lyrical_words = min(a)
        max_lyrical_words = max(a)
        average_lyrical_words = mean(a)
        json_dict = {
                'average' : average_lyrical_words,
                'min' : min_lyrical_words,
                'max' : max_lyrical_words
                }
        def make_corpus(dataset_main):
            # Initialize empty array 
            # to append clean text 
            corpus = [] 
        
            # rows to clean 
            for i in range(0, len(dataset_main['lyrics'])): 
                # column : "Review", row ith 
                review = dataset_main['lyrics'][i]
                review = re.sub(r'[^\w]', ' ', review)
        
                # convert all cases to lower cases 
                text = ' '.join([word for word in review.split() if word not in stopWords])
                corpus.append(text) 
            corpus_dataset = pd.DataFrame(corpus, columns=['lyrics'])
            return corpus, corpus_dataset
        
        corpus, corpus_dataset = make_corpus(dataset_main)
        
        def get_top_n_words(corpus, n=None):
            vec = CountVectorizer().fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in     vec.vocabulary_.items()]
            words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
            return words_freq[:n]
        
        word_freq = get_top_n_words(corpus, n=limit)
        result_df = pd.DataFrame(word_freq)
        result_df.columns = ['frequent_word', 'word_count']
        result_dict = result_df.to_dict()
        main_dict = {
                'words_info' : result_dict,
                'stat_info' : json_dict
                }
        return jsonify(main_dict)
    except:
        return jsonify({'trace': traceback.format_exc()})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=True)