from collections import Counter
from nltk.corpus import stopwords
import re



words = re.findall(r'\w+', open('ctecs.csv').read().lower());


most_common_words = Counter(words).most_common(10)

print 'Most common:'
for letter, count in most_common_words:
    print '%s: %7d' % (letter, count)
