import bz2
from collections import Counter

import spacy
from bs4 import BeautifulSoup
from spacy.parts_of_speech import PUNCT, SPACE, SYM


def is_word(tok):
    if tok.is_stop:
        return False
    if tok.pos in {PUNCT, SPACE, SYM}:
        return False

    text = tok.text
    if text in stop_words:
        return False

    # "that's" is tokenized to ["that", "'s"]
    return text[:1].isalnum()


def top_words(nlp, words, n=20):
    text = '\n'.join(words)
    doc = nlp(text)
    counts = Counter(tok.text.lower() for tok in doc if is_word(tok))
    total = sum(counts.values())
    for word, count in counts.most_common(40):
        percent = count / total * 100
        print(f'{word:<20}{percent:.2f}%')


nlp = spacy.load('en')
# Custom(?) stop words
stop_words = {'i', 'in', 'talk', 'we', 'the', 'it'}

with bz2.open('proposals.html.bz2') as fp:
    soup = BeautifulSoup(fp, 'lxml')

titles = soup('h4')
print(f'Total of {len(titles)} submissions')

title_words = [t.text.lower() for t in titles]
print('\nTitle words:')
top_words(nlp, title_words)

abstracts = soup('div', class_='session__abstract')
abstract_words = [a.text.lower() for a in abstracts]
print('\nAbstract words:')
top_words(nlp, abstract_words)

print('\nAll words:')
top_words(nlp, title_words + abstract_words)
