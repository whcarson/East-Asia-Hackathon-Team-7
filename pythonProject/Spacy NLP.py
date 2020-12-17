import nltk
import matplotlib
import json
import pandas as pd
import numpy as np
import sklearn as sk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix


def read_data(filename):
    return pd.read_csv(filename, delimiter='\t')


data = read_data('Restaurant_Reviews.tsv')

cleaned = []

for num in range(len(data)):
    rev = re.sub('[^a-zA-Z]', ' ', data['Review'][num])
    rev = rev.lower()
    rev = rev.split()
    portstem = PorterStemmer()
    rev2 = []
    for word in rev:
        if word not in set(stopwords.words('english')):
            rev2.append(word)
    rev = ' '.join(rev2)
    cleaned.append(rev)

token_lst = []

for rev in cleaned:
    token_lst.append(nltk.tokenize.word_tokenize(rev))

cv = CountVectorizer(max_features=1500)


def split(test_fraction):
    X = cv.fit_transform(cleaned).toarray()
    y = data.iloc[:, 1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_fraction)
    return X_train, X_test, y_train, y_test


def make_model(estimator_num, criterion, test_fraction):
    model = RandomForestClassifier(n_estimators=estimator_num, criterion=criterion)
    X = split(test_fraction)[0]
    y = split(test_fraction)[2]
    model.fit(X, y)
    return model


def fit_data(n, crit, fraction):
    predicted = make_model(n, crit, fraction).predict(split(fraction)[1])
    actual = split(fraction)[3]
    return confusion_matrix(actual, predicted), actual, predicted


