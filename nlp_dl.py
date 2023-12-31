# -*- coding: utf-8 -*-
"""NLP_DL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y5LZHlegCZE2WFS7m8azTSyJF3rnEXPY
"""

import numpy as np
import pandas as pd
import re

import tensorflow as tf
from tensorflow.keras.layers import Embedding, Dense, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

test= pd.read_csv('/content/SMS_test (2).csv',encoding='latin1')
train= pd.read_csv('/content/SMS_train (1).csv',encoding='latin1')

test

train

train.drop('S. No.',axis=1,inplace=True)
test.drop('S. No.',axis=1,inplace=True)

train.info()

test.info()

train.columns=['text','label']
test.columns=['text','label']

train['label']=train['label'].replace(['Spam','Non-Spam'],[1,0])
test['label']=test['label'].replace(['Spam','Non-Spam'],[1,0])

train

import string
def clean_text(text):
     # Remove special characters and numbers
    text = re.sub(r'[^A-Za-zÀ-ú ]+', '', text)

    # Convert to lower case
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

train['text'] = train['text'].apply(clean_text)
test['text'] = test['text'].apply(clean_text)

train

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer

def remove_stopwords(texto):
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(texto.lower())
    return " ".join([token for token in tokens if token not in stop_words])


train['text'] = train['text'].apply(remove_stopwords)
test['text'] = test['text'].apply(remove_stopwords)

def normalize_text(text):
    stemmer = SnowballStemmer("english")
    normalized_text = []
    for word in text.split():
        stemmed_word = stemmer.stem(word)
        normalized_text.append(stemmed_word)

    return ' '.join(normalized_text)


train['text'] = train['text'].apply(normalize_text)
test['text'] = test['text'].apply(normalize_text)

train

# Maximum number of words to be considered in the vocabulary
max_words = 10000
# Maximum number of tokens in a sequence
max_len = 200

tokenizer = Tokenizer(num_words = max_words)
tokenizer.fit_on_texts(train['text'])
# Converts texts into strings of numbers
sequences_train = tokenizer.texts_to_sequences(train['text'])
sequences_val = tokenizer.texts_to_sequences(test['text'])
# Mapping words to indexes
word_index = tokenizer.word_index

data_train = pad_sequences(sequences_train, maxlen = max_len)
data_val = pad_sequences(sequences_val, maxlen = max_len)

model = tf.keras.Sequential()
model.add(Embedding(max_words, 35, input_length = max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(64, activation = 'relu'))
# model.add(Dense(128, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

model.summary()

history = model.fit(data_train, train['label'], epochs = 15, batch_size = 64, validation_data = (data_val, test['label']))

model.save('/content/nlp.h5')

from tensorflow.keras.models import load_model
model = load_model('/content/nlp.h5')

def predict_text(text):
    # Apply the same preprocessing steps as during training
    text = clean_text(text)
    text = remove_stopwords(text)
    text = normalize_text(text)

    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)

    prediction = model.predict(padded_sequence)[0][0]

    return prediction


text_to_predict = "Congratulations! Upon reviewing your application, we would like to invite you to an interview.We have immediate job opening for the position of Data Analyst. Team is looking for good candidate with good knowledge. Team provide better offer according to Profile and location."
prediction = predict_text(text_to_predict)
print(f"Predicted Probability: {prediction}")

classification = 'spam' if prediction >= 0.5 else 'non spam'
print(f"Class: {classification}")

