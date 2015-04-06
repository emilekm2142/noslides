from django.conf.urls import patterns, include, url
from django.contrib import admin
from kwejk import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'noslides.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
     url(r'^$', views.showForm, name='form'),
    url(r'^out$', views.showGallery, name='gallery'),
    url(r'^send-request$', views.sendRequest, name='gallery'),
    url(r'^loadmore$', views.load_more, name='loadmore'),

)
