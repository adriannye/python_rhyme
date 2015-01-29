from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

# main angular view
from songrhyme.rhyme.views import IndexView

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rhyme/', include('rhyme.urls')),

    # everything else goes to main angular view.  This allows
    # any url to be entered into browser and angular will go to it.
    url(r'^.*$', IndexView.as_view(), name='index'),
)

