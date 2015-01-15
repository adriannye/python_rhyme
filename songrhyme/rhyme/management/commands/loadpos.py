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
        self.get_all()

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

    def get_all(self):
        counter = 0
        words = Word.objects.all()
        for word in words:
            if not counter % 100:
                print counter

            counter += 1

            # if any existing pos, remove them (from previous run)
            for pos in word.parts_of_speech.all():
                word.parts_of_speech.remove(pos)
            
            wordinfo = self.get_wordinfo(word.word)
            self.add_pos_m2m(word, wordinfo)

    def add_pos_m2m(self, word, wordinfo):
        for pos_name in wordinfo[word.word]['pos']:
            our_pos_name = self.get_our_pos_name(pos_name)
            word.parts_of_speech.add(self.pos[our_pos_name])
