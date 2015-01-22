from django.db import models
from accounts.models import Account
from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver

class PhonemeSequence(models.Model):
    """
    Represents the sequence of sounds that end a word.
    """
    text = models.CharField(max_length=255, db_index=True) 

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.text

    class Meta:
        ordering = ['text']


class RhymePhonemeSequence(models.Model):
    """
    Represents a phoneme sequence that rhymes in a certain way with
    the phoneme sequence for a word

    Essentially this relates a list of rhyme phoneme sequences to the 
    single phoneme sequence for the word.
    We relate to the phonemesequence, not the word, because more that one 
    word may have the same phoneme sequence.
    """
    FAMILY = 'FAMILY'
    ADDITIVE = 'ADDITIVE'
    SUBTRACTIVE = 'SUBTRACTIVE'
    RHYME_TYPES = (
        (FAMILY, 'Family'),
        (ADDITIVE, 'Additive'),
        (SUBTRACTIVE, 'Subtractive'),
    )

    sound = models.CharField(max_length=30) # user-visible description of sound
    original_ps = models.ForeignKey(PhonemeSequence, related_name='original_phoneme_sequences')
    rhyme_ps = models.ForeignKey(PhonemeSequence, related_name='rhyme_phoneme_sequences')
    rhyme_type = models.CharField(max_length=20, choices=RHYME_TYPES)
    order = models.IntegerField() 

    def __unicode__(self):  # Python 3: def __str__(self):
        return "%s %s-%s: %s" % (self.original_ps, self.rhyme_type, self.sound, self.order)


# Note: not in use.  TODO: delete
class PartOfSpeech(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Parts of Speech'

    def __unicode__(self):  # Python 3: def __str__(self):
            return self.name

NOUN = 0
VERB = 1
ADJECTIVE = 2
ADVERB = 3
PREPOSITION = 4
POS_CHOICES = (
    (NOUN, 'Noun'),
    (VERB, 'Verb'),
    (ADJECTIVE, 'Adjective'),
    (ADVERB, 'Adverb'),
    (PREPOSITION, 'Preposition'),
)

def ensure_list(value, delimiter=",", func=None):
    """Convert a value to a list, if possible.

    Args:
        value: a string of comma separated
            values - e.g. "1,2,3,4", but could be a list, a tuple, ...

        delimiter: string, the delimiter used to split the value argument,

        func: a function applied to each individual element in the list
            once the value arg is split. e.g. lambda x: int(x) would return
            a list of integers. Defaults to None - in which case you just
            get the list.

    Returns: a list if one can be parsed out of the input value. If the
             value input is an empty string or None, returns an empty
             list. If the split or func parsing fails, raises a ValueError.

    This is mainly used for ensuring the CSV model fields are properly
    formatted. Use this function in the save() model method and post_init()
    model signal to ensure that you always get a list back from the field.
    """

    if value in ["", u"", "[]", u"[]", u"[ ]", None]:
        return []

    if isinstance(value, list):
        l = value
    elif isinstance(value, tuple):
        l = list(value)
    elif isinstance(value, basestring) or isinstance(value, unicode):
        # TODO: regex this.
        value = value.lstrip('[').rstrip(']').strip(' ')
        if len(value) == 0:
            return []
        else:
            l = value.split(delimiter)
    elif isinstance(value, int):
        l = [value]
    else:
        raise ValueError(u"Unparseable smart_list value: %s" % value)

    try:
        func = func or (lambda x: x)
        return [func(e) for e in l]
    except Exception as ex:
        raise ValueError(u"Unable to parse value '%s': %s" % (value, ex))


class Word(models.Model):
    """
    Represents a word
    """
    word = models.CharField(max_length=255, unique=True, db_index=True)
    phoneme_sequence = models.ForeignKey(PhonemeSequence)
    # pos is not a ManyToMany because it makes the desired queries 
    # difficult since prefetch_related doesn't work with a filtered queryset.
    pos = models.CommaSeparatedIntegerField(max_length=255, choices=POS_CHOICES, default='')

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.word

    def add_pos(self, pos):
        """
        Take int or string value and add to list
        """
        self.pos = self.pos + ',%s' % pos
        self.save()

    def has_pos(self, pos):
        """
        Return True if int or string pos is in pos field
        """
        pos = str(pos)
        pos_list = self.pos.split(',')
        return pos in pos_list

    @classmethod
    def words_containing_pos(self, pos):
        return Word.objects.filter( Q(pos__startswith=pos+',') | Q(pos__endswith=','+pos) | Q(pos__contains=',{0},'.format(pos)) | Q(pos__exact=pos) )

    def clean_pos(self):
        """Convert CommaSeparatedIntegerField string values to list."""
        func = lambda x: int(x)
        self.pos = ensure_list(self.pos, func=func)

@receiver([pre_save, post_init], sender=Word)
def _on_model_signal(sender, instance, **kwargs):
    instance.clean_pos()
    class Meta:
        ordering = ['word']


class PeerReview(models.Model):
    """
    Represents review status of a word.
    Views that modify this require login.
    """
    user_added = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(Account)
    word = models.OneToOneField(Word)

    def __unicode__(self):  # Python 3: def __str__(self):
        return "user_added: %s flagged: %s reviewed: %s paid: %s" % \
                (self.user_added, self.flagged, self.reviewed, self.paid)
