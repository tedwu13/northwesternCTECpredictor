from collections import Counter
from nltk.corpus import stopwords
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from collections import defaultdict
import csv
import re
import json
import os.path





def readCTEC(data_file):
    columns = defaultdict(list) # each value in each column is appended to a list
    with open(data_file) as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k
    ctecs_essay = columns['essay']
    ctec_score = columns['question0_average_rating']
    return ctecs_essay, ctec_score


def preprocess(data_file, bag):
    data = []
    reviews, scores = readCTEC(data_file)
    for idx, review in enumerate(reviews):
        review = re.findall(r'[a-z]+', review.lower())

        word_array = [0]*5000
        for word in review:
            if word in bag:
                word_array[bag[word]] = 1
        data.append(word_array)

    return data, scores


if not os.path.exists("bag.json"):
    print "not found, building"
    # generate a list of words by enumerating over all CTECs
    words = re.findall(r'[a-z]+', open('ctecs.csv').read().lower());
    print words
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
        bag = json.dump(bag, fp)
else:
    print "found, importing"
    bag = {}
    with open('bag.json') as fp:
        bag = json.load(fp)

data, scores = preprocess('ctecs.csv', bag)
ds = SupervisedDataSet(5000, 1)

for idx, example in enumerate(data):
    if scores[idx]:
        ds.addSample(example, (float(scores[idx]),))

net = buildNetwork(5000, 3, 1, bias=True)
trainer = BackpropTrainer(net, ds)
print trainer.train()
