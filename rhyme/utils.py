
from nltk.corpus import wordnet

# Note: Brown, CMUdict, and Wordnet Corpora were installed, but only
# wordnet is used here.
class WordNet(object):
    """
    Get list of parts of speech, definitions and synonyms from Wordnet
    """
    word_info = {}

    def __init__(self, word):
        self.word = word

        # only search if we haven't already
        if word not in self.word_info:
            self.word_info[word] = {
                'pos': set(),
                'definitions': [],
                'synonyms': set(),
            }
            self.synsets = wordnet.synsets(word)
            self.extract()

    def extract(self):
        for synset in self.synsets:
            self.word_info[self.word]['pos'].add(self.lex_type_to_pos(synset.lexname()))
            self.word_info[self.word]['definitions'].append(synset.definition())
            for syn in self.clean_lemma(synset.lemma_names()):
                self.word_info[self.word]['synonyms'].add(syn)

    def lex_type_to_pos(self, lex_type):
        """
        wordnet conflates the pos with other stuff which has to be removed
        """
        parts = lex_type.split('.')
        return parts[0].title()

    def clean_lemma(self, lemma):
        """
        wordnet includes the original word in synonym list: remove it
        """
        try:
            lemma.remove(self.word)
        except:
            pass

        return lemma
