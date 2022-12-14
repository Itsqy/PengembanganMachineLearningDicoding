# -*- coding: utf-8 -*-
"""NLP Text Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sJIDPr05fFjBHqepd6TgJlkMA88slel1
"""

pip install -q kaggle

# upload kaggle.json
from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!ls ~/.kaggle

# test kaggle dataset list
!kaggle datasets list

!wget --no-check-certificate \
  https://storage.googleapis.com/dataset-uploader/bbc/bbc-text.csv \
  -O /tmp/bbc-text.csv

import pandas as pd
df = pd.read_csv('/tmp/bbc-text.csv')
df



df = pd.read_csv('reviewArchives/Women Dresses Reviews Dataset .csv', sep='\t')

df.head(9)

df.columns

import nltk, os, re, string

from keras.layers import Input, LSTM, Bidirectional, SpatialDropout1D, Dropout, Flatten, Dense, Embedding, BatchNormalization
from keras.models import Model
from keras.callbacks import EarlyStopping
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical


from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

nltk.download('wordnet')

# data category one-hot-encoding
category = pd.get_dummies(df.category)
df_with_category = pd.concat([df, category], axis=1)
df_with_category = df_with_category.drop(columns='category')
df_with_category.head(10)

df_with_category.text = df_with_category.text.apply(lambda x: x.lower())


def cleaner(data):
    return(data.translate(str.maketrans('','', string.punctuation)))
    
    df_with_category.text = df_with_category.text.apply(lambda x: lem(x))


lemmatizer = WordNetLemmatizer()
def lem(data):
    pos_dict = {'N': wn.NOUN, 'V': wn.VERB, 'J': wn.ADJ, 'R': wn.ADV}
    return(' '.join([lemmatizer.lemmatize(w,pos_dict.get(t, wn.NOUN)) for w,t in nltk.pos_tag(data.split())]))
    df_new.title = df_new.title.apply(lambda x: lem(x))
    df_new.content = df_new.content.apply(lambda x: lem(x))


def rem_numbers(data):
    return re.sub('[0-9]+','',data)
    df_with_category['text'].apply(rem_numbers)

# total data
df_with_category.head(10)

text = df_with_category['text'].values
labeling = df_with_category[['business', 'entertainment', 'politics', 'sport', 'tech']].values

text

labeling

from sklearn.model_selection import train_test_split
text_train, text_test, labeling_train, labeling_test = train_test_split(text, labeling, test_size=0.2, shuffle=True)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
 
tokenizer = Tokenizer(num_words=5000, oov_token='x', filters='!"#$%&()*+,-./:;<=>@[\]^_`{|}~ ')
tokenizer.fit_on_texts(text_train) 
tokenizer.fit_on_texts(text_test)
 
train_seq = tokenizer.texts_to_sequences(text_train)
test_seq = tokenizer.texts_to_sequences(text_test)
 
train_pad = pad_sequences(train_seq) 
test_pad = pad_sequences(test_seq)

import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=64),
    tf.keras.layers.LSTM(128),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(5, activation='softmax')
])
model.compile(optimizer='adam', metrics=['accuracy'], loss='categorical_crossentropy',)
model.summary()

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.9 and logs.get('val_accuracy')>0.9):
      self.model.stop_training = True
      print("\n akurasi dah sampe 90% lebih nih")
callbacks = myCallback()

# model fit
history = model.fit(train_pad, labeling_train, epochs=66, 
                    validation_data=(test_pad, labeling_test), verbose=2, callbacks=[callbacks], validation_steps=30)