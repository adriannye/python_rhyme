from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings
from rest_framework import routers

from rhyme.views import *

#router = routers.DefaultRouter()
#router.register(r'ps', PhonemeSequenceViewSet)
#router.register(r'rps', RhymePhonemeSequenceViewSet)

urlpatterns = patterns('rhyme.views',
    #url(r'^', include(router.urls)),
    url('^rhyme_ps/(?P<word>.+)/$', ListRhymePhonemeSequences.as_view()),
    url('^rhymes/(?P<ps>.+)/$', ListRhymes.as_view()),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
