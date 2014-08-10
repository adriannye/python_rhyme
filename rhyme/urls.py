from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.conf import settings

from rhyme.views import *
admin.autodiscover()

urlpatterns = patterns('rhyme.views',
    #    url(r'^add/$', AddCan(), name='add-can'),
    )

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
