from collection import Counter
from nltk.corpus import stopwords
import re





words = re.findall(r'\w+', open('ctecs.csv').read().lower());

Counter(words).most_common(10)