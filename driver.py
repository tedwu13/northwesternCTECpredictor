from collections import Counter
from nltk.corpus import stopwords
import re
import json

# generate a list of words by enumerating over all CTECs
words = re.findall(r'[a-z]+', open('ctecs.csv').read().lower());

# stop words
stop = stopwords.words('english')
customized_stop_words = []

# organize by count
most_common_words = Counter(words).most_common(5000 + len(stop))

bag = {}
index = 0
for word, count in most_common_words:
    if word not in stop:
    	bag[word] = index
        index += 1
    if index == 5000:
        break
# dump a bag of words of the 5000 most common words across CTECs
with open('bag.json', 'w') as fp:
    json.dump(bag, fp)
