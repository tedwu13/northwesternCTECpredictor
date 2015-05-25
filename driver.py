from collections import Counter
from nltk.corpus import stopwords
import re



words = re.findall(r'\w+', open('ctecs.csv').read().lower());


most_common_words = Counter(words).most_common(5000)
stop = stopwords.words('english')
customized_stop_words = []

print 'Most common:'
for letter, count in most_common_words:
    if letter not in stop and letter.isdigit() == False:
    	print '%s: %7d' % (letter, count)




