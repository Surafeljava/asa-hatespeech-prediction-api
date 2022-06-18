import os
# from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from aiohttp import ClientSession

from amharic_filter import AmharicFilter
from utils import Utils

# import joblib
# import tensorflow as tf
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


# async def get_data(seconds):
#     endpoint = f'delay/{seconds}'

#     print(f'Getting data with {seconds} seconds delay')

#     async with ClientSession() as session:
#         async with session.get(f'{baseUrl}{endpoint}') as response:
#             return await response.json()


@app.route('/')
async def home():
    return "Hello World"


# @app.route('/check')
# @cross_origin()
# def check():
#     tf.saved_model.LoadOptions(
#         experimental_io_device=None
#     )
#     tokenizer = Tokenizer(num_words=5000)

#     new_model = tf.keras.models.load_model('./my_model')

#     test_word = "የጉራጌ ዘር ከሃዲ ነው።"

#     tw = tokenizer.texts_to_sequences([test_word])
#     tw = pad_sequences(tw, maxlen=200)

#     return new_model.predict(tw).item()


# @app.route('/checkhate', methods=['GET', 'POST'])
# @cross_origin()
# async def checkhate():
#     if request.method == 'GET':
#         data = await get_data(2)
#         return data
#     if request.method == 'POST':
#         data = request.json
#         return data
#     else:
#         return 'Invalid request'


async def get_address(address):
    endpoint = f'?address={address}&key=AIzaSyABPEzN748CdxwYb0FHLP9RTkZ7-FE_4pw'

    # headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAJ0PXQEAAAAAHBTso%2BOW1k6V5kgGzCfIGLMbUpg%3DvXjswixg0EJ3sgt1uBL78uyeJDfwyAcpXkHjE34aaPsBc07pv6"}
    async with ClientSession() as session:
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


# @app.route('/predict', methods=['POST'])
# @cross_origin()
def predict(sentence):
    prediction = 0
    prediction = predict_from_sentence(sentence)
    return prediction


@app.route('/gettweetdata', methods=['GET', 'POST'])
async def get_tweet_data():
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
        address = d['country']
        if address != '':
            # Add the new location
            loc = await get_address(address)
            l = loc['results'][0]['geometry']['location']
            amf.setLocation(l)

        print(amf.getData())

        try:
            pr = predict(normalized)
            return jsonify({'sentence': normalized, 'prediction': pr, 'tweet_data': amf.getData()}), 200
        except Exception as e:
            return jsonify({'sentence': normalized, 'error': e}), 400

        # return jsonify({'some': 'data'})


if __name__ == '__main__':
    app.run(debug=True)
