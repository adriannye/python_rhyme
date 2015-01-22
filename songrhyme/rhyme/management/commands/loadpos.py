from django.core.management.base import BaseCommand

from rhyme.models import *
from rhyme.utils import WordNet

class Command(BaseCommand):
    help = "load word info such as part of speech"

    pos_names = set()

    
    def handle(self, *args, **options):
        poses = PartOfSpeech.objects.all()
        self.pos = {}
        for pos in poses:
            self.pos[pos.name] = pos
        self.load_all_words()
        #self.test()

    def get_our_pos_code(self, name):
        "translate wordnet name for pos to our code"
        if name == 'Adj':
            return ADJECTIVE
        elif name == 'Adv':
            return ADVERB
        elif name == 'Noun':
            return NOUN
        elif name == 'Verb':
            return VERB
        elif name == 'Preposition':
            return PREPOSITION
        else:
            raise Exception('Unexpected wordnet part of speech string')

    def get_our_pos_name(self, name):
        "translate wordnet name for pos to our name"
        if name == 'Adj':
            return 'Adjective'
        elif name == 'Adv':
            return 'Adverb'
        else:
            return name

    def test(self):
        word = Word.objects.get(word='approach')
        wordinfo = self.get_wordinfo(word.word)
        self.add_pos_m2m(word, wordinfo)

    def get_wordinfo(self, word):
        wordnet = WordNet(word)

        return wordnet.word_info

    def load_all_words(self):
        counter = 0
        words = Word.objects.all()
        for word in words:
            if not counter % 100:
                print counter

            counter += 1

            wordinfo = self.get_wordinfo(word.word)
            self.add_pos_m2m(word, wordinfo)

    def add_pos_m2m(self, word, wordinfo):
        word.pos = []
        # wordinfo[word.word] contains 'definitions', 'synonyms', and 'pos'
        for pos_name in wordinfo[word.word]['pos']:
            pos_code = self.get_our_pos_code(pos_name)
            word.pos.append(pos_code)
            #word.parts_of_speech.add(self.pos[our_pos_name])
        for synonym_str in wordinfo[word.word]['synonyms']:
            try:
                synonym = Word.objects.get(word=synonym_str)
            except Word.DoesNotExist:
                continue

            word.synonyms.add(synonym)
        word.save()
