from django.contrib import admin

# Register your models here.

from django.contrib import admin
from rhyme.models import PeerReview, PhonemeSequence, RhymePhonemeSequence, PartOfSpeech, Word

admin.site.register(PeerReview)
admin.site.register(PhonemeSequence)
admin.site.register(RhymePhonemeSequence)
admin.site.register(PartOfSpeech)
admin.site.register(Word)
