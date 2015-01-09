from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rhyme.models import *
from rhyme.utils import WordNet

class Command(BaseCommand):
    help = "load word info such as part of speech"

    def handle(self, *args, **options):
        poses = PartOfSpeech.objects.all()
        self.pos = {}
        for pos in poses:
            self.pos[pos.name] = pos
        #self.get_all()
        self.test()

    def test(self):
        #word = Word.objects.get(word='bond')
        word = Word.objects.get(word='approach')
        wordinfo = self.get_wordinfo(word.word)
        print wordinfo

    def get_wordinfo(self, word):
        print word
        wordnet = WordNet(word)

        return wordnet.word_info

    def get_all(self):
        counter = 0
        words = Word.objects.all()
        for word in words:
            if not counter % 100:
                print counter

            counter += 1
            
            wordinfo = self.get_wordinfo(word.word)
            # TODO save db items
