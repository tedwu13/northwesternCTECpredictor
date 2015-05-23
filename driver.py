from collections import Counter
from nltk.corpus import stopwords
import re





words = re.findall(r'\w+', open('ctecs.csv').read().lower());
# count the most common words 

most_common_words = Counter(words).most_common(10)

print most_common_words
#stop = stopwords.words('english')


