import os
import re
import numpy as np
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import random


class Generator:
    def __init__(self, fraction_reviews, file_path):
        self.fraction = fraction_reviews
        self.fp = file_path

    def combine_reviews(self):
        reviewstr = ""
        for filename in os.listdir(self.fp):
            if random.random() < self.fraction:
                with open(self.fp + "/" + filename, 'r') as fh:
                    try:
                        lines = fh.readlines()
                    except UnicodeDecodeError:
                        lines = ["", ""]
                string1 = "".join(lines)
                string2 = re.sub('<br />', "", string1)
                string3 = re.sub('[^0-9a-zA-Z ]+', '', string2)
                reviewstr += string3
        return reviewstr

    def tokenize(self):
        combined = self.combine_reviews()
        string = combined.lower()
        tokenizer = RegexpTokenizer(r'\w')
        tokens = tokenizer.tokenize(string)
        stop_words = stopwords.words('english')
        tokens = [token for token in tokens if token not in stop_words]
        new_str = " ".join(tokens)
        return new_str

    def make_char_dict(self):
        chars = sorted(list(set(self.tokenize())))
        num_dict = dict((char, index) for index, char in enumerate(chars))
        return chars, num_dict

    def generate_x_and_y(self, seq_length=100):
        n_dict = self.make_char_dict()[1]
        processed = self.tokenize()
        in_len = len(processed)
        print(in_len)
        dict_len = len(self.make_char_dict()[0])
        x = []
        y = []
        for num in range(0, in_len - seq_length):
            in_seq = processed[num:num + seq_length]
            out_char = processed[num + seq_length]
            x.append([n_dict[char] for char in in_seq])
            y.append(n_dict[out_char])
        return x, y, dict_len

    def to_array(self, length=100):
        x, y, dict_len = self.generate_x_and_y(seq_length=length)
        X = np.reshape(x, (len(x), length, 1))
        X = X / dict_len
        y = np_utils.to_categorical(y)
        return X, y

    def form_model(self, length=100):
        X, y = self.to_array(length=length)
        model = Sequential()
        model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(256, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(128))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        filepath = "model_weights_saved.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        desired_callbacks = [checkpoint]
        return model, desired_callbacks, X, y

    def fit_model(self, length=100):
        model, cp, X, y = self.form_model(length=length)
        model.fit(X, y, epochs=4, batch_size=256, callbacks=cp)
        model.save("saved_model")
        return model

    def load_model(self, length=100):
        model = self.form_model(length=length)[0]
        model.load_weights("model_weights_saved.hdf5")
        model.compile(loss='categorical_crossentropy', optimizer='adam')