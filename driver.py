from collection import Counter
import re

words = re.findall(r'\w+', open('ctecs.csv').read().lower());

Counter(words).most_common(10)