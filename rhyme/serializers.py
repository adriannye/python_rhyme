from rest_framework import serializers

from rhyme.models import RhymePhonemeSequence, PhonemeSequence, PeerReview, PartOfSpeech, Word

class PartOfSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartOfSpeech
        fields = ('name')

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('word', 'parts_of_speech')

class PhonemeSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhonemeSequence
        fields = ('text',)

class RhymePhonemeSequenceSerializer(serializers.ModelSerializer):
    rhyme_ps = serializers.SlugRelatedField(read_only=True,
                                                      slug_field='text')
    original_ps = serializers.SlugRelatedField(read_only=True,
                                                      slug_field='text')
    class Meta:
        model = RhymePhonemeSequence
        fields = ('original_ps', 'sound', 'rhyme_ps', 'rhyme_type', 'order')

class PeerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerReview
        fields = ('user_added', 'flagged', 'reviewed', 'groups')

