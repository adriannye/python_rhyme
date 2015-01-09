from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rhyme.management.commands.w2pdec import word2phonemeseqdict
from rhyme.management.commands.p2rdec import phoneme2rhymedict
from rhyme.models import *

class Command(BaseCommand):
    help = "load db with initial data."

    def handle(self, *args, **options):
        self.test = options.get('test', False)
        self.user = User.objects.get(username='admin')
        self.add_perfect_rhymes()

    def add_perfect_rhymes(self):
        counter = 0
        if self.test:
            rhyme_dict = {
                    '.D': phoneme2rhymedict['.D'],  # node, etc
                    '.N': phoneme2rhymedict['.N'],  # bone, etc
                    '.': phoneme2rhymedict['.'],  # below, etc
                    '_*': phoneme2rhymedict['_*'],  # belong, etc
                    '(ND': phoneme2rhymedict['(ND'],  # pond, etc
            }
        else:
            rhyme_dict = phoneme2rhymedict
        for phoneme_seq, rhyme_list in rhyme_dict.iteritems():
            if not counter % 100:
                print counter

            counter += 1

            ps, created = PhonemeSequence.objects.get_or_create(
                text=phoneme_seq
            )
            for word in rhyme_list:
                try:
                    word = Word.objects.get(
                        word=word,
                        phoneme_sequence=ps,
                    )
                except: 
                    word = Word.objects.create(
                        word=word,
                        phoneme_sequence=ps,
                    )
                    word.save()
                    pr = PeerReview.objects.create(
                        word_id=word.id,
                        added_by=self.user,
                        reviewed=True,
                        paid=True,
                    )
                    pr.save()

