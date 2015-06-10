from collections import Counter
from nltk.corpus import stopwords
import csv
import re
import json
import os.path
import time

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

        word_array = [0]*500
        for word in review:
            if word in bag:
                word_array[bag[word]] = 1
        data.append(word_array)

    return data, scores

# if a bag doesn't exist, create it
if not os.path.exists("bag.json"):
    print "bag not found, building"
    # generate a list of words by enumerating over all CTECs
    words = re.findall(r'[a-z]+', open('ctecs.csv').read().lower())

    # stop words
    stop = stopwords.words('english')

    # organize by count
    most_common_words = Counter(words).most_common(500 + len(stop))

    bag = {}
    index = 0
    for word, count in most_common_words:
        if word not in stop:
            bag[word] = index
            index += 1
        if index == 500:
            break

    # add professors
    professors = []
    with open('ctecs.csv') as f:
        for line in f:
            if len(line.split(",")) < 12:
                continue
            professor = line.split(",")[11]
            if not professor:
                continue

            professors.append(professor)

    most_common_professors = Counter(professors).most_common(500)

    for professor, count in most_common_professors:
        professor = professor.replace('\'','')
        bag[professor] = index
        index += 1


    # dump a bag of words of the 5000 most common words across CTECs
    with open('bag.json', 'w') as fp:
        json.dump(bag, fp)
else:
    print "found, importing"
    # otherwise, load from file
    bag = {}
    with open('bag.json') as fp:
        bag = json.load(fp)

# generate a weka file, starting with the header
weka = open('ctecs.arff', 'w')
weka.write('@relation training\n')
weka.write('\n')

for item in sorted(bag.items(), key=lambda x: x[1]):
    weka.write('@attribute \'' + item[0] + '\' {0, 1}\n')
weka.write('@attribute \'ctec_score\' {0, 1}\n')
weka.write('\n')

weka.write('@data\n')
with open('ctecs.csv') as f:
    firstline = True
    for line in f:
        if firstline:
            firstline = False
            continue

        if not line:
            continue

        if len(line.split(',')) < 18:
            continue

        score = line.split(',')[17]
        if not score:
            continue

        test = re.findall(r'[a-z:]', score)
        if len(test) > 0:
            continue

        if float(score) > 6:
            continue

        if float(score) > 5:
            score = 1
        else:
            score = 0

        ctec_array = [0] * 1000
        words = re.findall(r'[a-z]+', line.lower())
        for word in words:
            if word in bag:
                ctec_array[bag[word]] = 1

        professor = line.split(',')[11]
        if professor in bag:
            ctec_array[bag[professor]] = 1

        if sum(ctec_array) == 0:
            continue

        for word in ctec_array:
            weka.write(str(word) + ',')
        weka.write(str(score) + '\n')
