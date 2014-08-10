
class PeerReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PeerReview
        fields = ('user_added', 'flagged', 'reviewed', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
