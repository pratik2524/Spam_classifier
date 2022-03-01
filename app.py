import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
import sklearn


def transform_text(text):
    # lowercase
    text = text.lower()
    # Tokenization
    text = nltk.word_tokenize(text)
    # removing special characters
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

#Title of the page

st.title("Email/SMS Classifier")

input_msg = st.text_area("enter the message")
if st.button('Check'):
    #preprocessing
    transformed_msg = transform_text(input_msg)
    #vectorization
    vector = tfidf.transform([transformed_msg])
    #prediction
    result = model.predict(vector)[0]
    #display
    if result==1:
        st.header("Spam")
    else:
        st.header("Not Spam")
