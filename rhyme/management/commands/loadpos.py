import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

#from rhyme.management.commands.w2pdec import word2phonemeseqdict
#from rhyme.management.commands.p2rdec import phoneme2rhymedict
from rhyme.models import *

class Command(BaseCommand):
    help = "load db with initial data."

    def handle(self, *args, **options):
        self.add_pos()

    def mk_pos_dict(self):
        """
        In result_dict:
        keys are letters using in Moby POS

        Values are corresponding django objects
        """
        # simplify the 15 pos from moby to 9
        moby_key_simplification = {
            'N': 'Noun',
            'p': 'Plural',
            'h': 'Noun',
            'V': 'Verb',
            't': 'Verb',
            'i': 'Verb',
            'A': 'Adjective',
            'v': 'Adverb',
            'C': 'Conjunction',
            'P': 'Preposition',
            '!': 'Interjection',
            'r': 'Pronoun',
            'D': 'Article',
            'I': 'Article',
            'o': 'Noun',
        }
        poss = PartOfSpeech.objects.all()
        pos_dict = {}
        for p in poss:
            pos_dict[p.name] = p

        result_dict = copy(moby_key_simplification)
        for key, value in result_dict.iteritems():
            result_dict[key] = pos_dict[value]

        return pos_dict
        

    def add_pos(self):
        pos_file = os.path.join(settings.BASEDIR, 'rhyme', 'management', 'commands', 'mobypossrc.txt')
        pos_dict = self.mk_pos_dict()
        with open(pos_file, 'r') as f:
            pos = []
            linecount = 0
            print "running pos"
            for line in f.readlines():
                line = line.strip()
                substrings = line.split("\\") # split into word and pos (at \)
                word = substrings[0].lower()
                pos = list(substrings[1])
                try:
                    word_obj = Word.objects.get(word=word)
                except Word.DoesNotExist:
                    print 'not found: ', word
                    continue

                for part in pos:
                    word_obj.parts_of_speech.add(pos_dict[part])

