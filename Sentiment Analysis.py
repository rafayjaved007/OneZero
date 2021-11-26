import requests
import json
import nltk
import re
import collections
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


def convert_to_lower(product):
    lower_reviews = []
    for review in product['reviews']:
        lower_reviews.append(review.lower())
    product['reviews'] = lower_reviews
    return product


def get_adjectives(clean_text_5):
    adjectives = []
    for words in clean_text_5:
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(words))):
            # checking if it is an adjective or not
            if pos == 'JJ' or pos == 'JJR' or pos == 'JJS':
                adjectives.append(word)
    return adjectives


def clean3(clean_text_2):
    clean_text_3 = []
    for words in clean_text_2:
        clean = []
        for w in words:
            res = re.sub(r'[^\w\s]', "", w)
            if res != "":
                clean.append(res)
        clean_text_3.append(clean)
    return clean_text_3


def clean4(clean_text_3):
    clean_text_4 = []
    for words in clean_text_3:
        w = []
        for word in words:
            if not word in stopwords.words('english'):
                w.append(word)
        clean_text_4.append(w)
    return clean_text_4


def clean5(clean_text_4):
    clean_text_5 = []
    for words in clean_text_4:
        for word in words:
            clean_text_5.append(word)
    return clean_text_5


def getAnalysis(score):
    if score < 0 and score >= -0.5:
        return 'Negative'
    elif score < -0.5:
        return 'Very Negative'
    elif score == 0:
        return 'Neutral'
    elif score > 0 and score <= 0.5:
        return 'Positive'
    else:
        return 'Very Positive'


def process(product, daraz):
    clean_text_1 = convert_to_lower(product)
    clean_text_2 = [word_tokenize(i) for i in clean_text_1['reviews']]
    clean_text_3 = clean3(clean_text_2)
    clean_text_4 = clean4(clean_text_3)
    clean_text_5 = clean5(clean_text_4)

    makeitastring = ''.join(map(str, clean_text_5))
    blob = TextBlob(makeitastring)
    clean_text_6 = get_adjectives(clean_text_5)

    word_counter = []
    word_counts = collections.Counter(clean_text_6)
    for word, count in sorted(word_counts.items()):
        word_counter.append({word: count})

    product.pop('reviews')
    product['polarity'] = getAnalysis(blob.sentiment.polarity)
    product['word_counter'] = json.dumps(word_counter)
    product['website'] = daraz
    if 'http' not in product['product_url']:
        product['product_url'] = 'http:' + product['product_url']
    if product['sale_price'] == '':
        product['sale_price'] = 0

    requests.post('http://127.0.0.1:8000/core/products/', data=product)


###### Starting Point #######
file = open('daraz.json')
products = json.load(file)
for product in products:
    process(product, 'Daraz.pk')
