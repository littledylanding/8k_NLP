import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in stop_words]
    words = [re.sub(r'([a-zA-Z])(\d)', r'\1 \2', word) for word in words]
    words = [re.sub(r'(\d)([a-zA-Z])', r'\1 \2', word) for word in words]
    return words


def count_categories(words):
    category_counts = {category: 0 for category in categories}
    for word in words:
        if word.upper() in dictionary.index:
            word_data = dictionary[dictionary.index == word.upper()]
            for category in categories:
                if word_data[category].values[0]:
                    category_counts[category] += 1
    return pd.Series(category_counts)


dictionary = pd.read_csv('Loughran-McDonald_MasterDictionary_1993-2021.csv', index_col=0)
data = pd.read_csv('df_item.csv')
data['tokenized'] = data['Content'].apply(preprocess_text)
categories = dictionary.columns[6:13]
category_counts = data['tokenized'].apply(count_categories)
data = pd.concat([data, category_counts], axis=1)
data.to_csv('bagofwords.csv')
