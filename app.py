import os
# from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from aiohttp import ClientSession
from datetime import date

from amharic_filter import AmharicFilter
from utils import Utils
import random
# import joblib
# from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

import pickle

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["MKLDNN_VERBOSE"] = "1"

ut = Utils()

app = Flask(__name__)

baseUrl = 'http://httpbin.org/'
addressBaseUrl = 'https://maps.googleapis.com/maps/api/geocode/json'


# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
async def home():
    return "Hello World"


async def get_address(address):
    endpoint = f'?address={address}&key=AIzaSyABPEzN748CdxwYb0FHLP9RTkZ7-FE_4pw'

    # headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAJ0PXQEAAAAAHBTso%2BOW1k6V5kgGzCfIGLMbUpg%3DvXjswixg0EJ3sgt1uBL78uyeJDfwyAcpXkHjE34aaPsBc07pv6"}
    async with ClientSession(trust_env=True) as session:
        async with session.get(f'{addressBaseUrl}{endpoint}') as response:
            return await response.json()

model = load_model('./asa_model.h5')


def predict_from_sentence(sentence):

    with open('asa_tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # Create a token for the work
    token = tokenizer.texts_to_sequences([sentence])
    tw = pad_sequences(token, maxlen=256)
    # tw = token

    # Predict with the model
    prediction = model.predict(tw).item()
    print('\n', sentence, '\n', prediction)

    return prediction
    # return "Prediction Result here"


@app.route('/predict_from_text', methods=['POST'])
def predict():
    try:
        data = request.json
        sentence = data['sentence']
        prediction = -1
        prediction = predict_from_sentence(sentence)
        return jsonify({'sentence': sentence, 'prediction': prediction}), 200
    except Exception as e:
        return jsonify({'sentence': sentence, 'error': e}), 400


@app.route('/predict_from_username', methods=['POST'])
async def predict_from_username():
    try:
        data = request.json
        username = data['username']
        # recent = data['recent']

        # Fetch user posts
        amf = AmharicFilter()
        res = await amf.get_tweet_by_username(username)

        if len(res) < 0:
            return jsonify({'error': 'No post for this username'}), 400

        # print(res)

        # Only choosing the recent 5 posts of the user
        recent_five = [{'tweetId': a.get('id'), 'text': a.get('text'),
                        'country': a['user'].get('location'), 'dateOfTweet': a.get('created_at')} for a in res[0:5]]

        # print(recent_five)

        contains_hate = []

        for tw in recent_five:

            if not tw['text']:
                continue

            # update sentence with the one fetched from the API
            amf.setData(tw['text'], tw['country'])
            d = amf.getData()

            is_amh = amf.checkIfAmharic()
            if not is_amh:
                continue

            # remove non amharic letters
            all_amh = amf.removeNonAmharic()

            # normalize the sentence
            normalized = amf.normalize()

            # Check for hate speech here
            hate_check_res = predict_from_sentence(normalized)

            # Check if it has country or city name
            address = amf.getData()['country'] + ''
            if address != '':
                # Add the new location
                loc = await get_address(address)
                l = loc['results'][0]['geometry']['location']
                amf.setLocation(l['lat'], l['lng'])

            # Update the text with the normalized one
            tm = tw
            tm['text'] = normalized
            tm['hateValue'] = hate_check_res
            tm['dateOfPrediction'] = date.today().strftime("%b-%d-%Y")
            tm['loc_lat'] = amf.getData()['lat'] + random.randint(2, 8)
            tm['loc_lng'] = amf.getData()['lng'] + random.randint(1, 5)
            # tm['dateOfTweet'] = hate_check_res['prediction']
            contains_hate.append(tm)
            # print(amf.check_hatespeech())

        new_tweets = []

        # for all in contains_hate: check if already collected
        for tweet in contains_hate:
            check = await amf.check_if_tweet_collected_before(tweet['tweetId'])
            if check and tweet['hateValue'] > 0.49 and tweet['country'] != '':
                new_tweets.append(tweet)

        # print(new_tweets)

        # for all in contains_hate: save them to the database
        for tweet_info in new_tweets:
            res = await amf.save_to_hate_collection(tweet_info)
            print(res, '\n')

        return jsonify({'alltweet': contains_hate}), 200
    except Exception as e:
        return jsonify({'error': e}), 400


@app.route('/predict_from_tweetid', methods=['GET', 'POST'])
async def predict_from_tweetid():
    if request.method == 'GET':
        return jsonify({'message': 'Method Not Allowed'}), 405
    if request.method == 'POST':
        data = request.json
        t_id = data['tweet_id']

        validTweetId = ut.checkIfValidTweetId(t_id)

        if not validTweetId:
            return jsonify({'status': 'error', 'message': 'Invalid tweet id'}), 404

        amf = AmharicFilter()
        res = await amf.get_data(t_id)

        if not res:
            return jsonify({'status': 'error', 'message': 'Invalid tweet id'}), 401

        # update sentence with the one fetched from the API
        amf.setData(res['text'], res['user']['location'])
        d = amf.getData()

        # check if it contains amharic sentence
        is_amh = amf.checkIfAmharic()
        if not is_amh:
            return jsonify({'status': 'error', 'message': 'Does not contain an amharic sentence or phrase'}), 401

        # normalize the sentence
        normalized = amf.normalize()

        # Check if it has country or city name

        print(res)

        address = d['country']
        if address != '':
            # Add the new location
            loc = await get_address(address)
            l = res['geometry']['location']
            amf.setLocation(l['lat'], l['lng'])

        print(amf.getData())

        try:
            pr = predict_from_sentence(normalized)

            data = {
                'tweetId': t_id,
                'text': normalized,
                'hateValue': pr,
                'dateOfPrediction': date.today().strftime("%b-%d-%Y"),
                'loc_lat': amf.getData()['lat'],
                'loc_lng': amf.getData()['lng'],
                'country': res['user'].get('location'),
                'dateOfTweet': res.get('created_at')
            }

            check = await amf.check_if_tweet_collected_before(t_id)
            if check and pr > 0.49 and data['country'] != '':
                res = await amf.save_to_hate_collection(data)
                # new_tweets.append(tweet)

            return jsonify({'sentence': normalized, 'prediction': pr, 'tweet_data': amf.getData()}), 200
        except Exception as e:
            return jsonify({'sentence': normalized, 'error': e}), 400

        # return jsonify({'some': 'data'})


if __name__ == '__main__':
    app.run(debug=True)
