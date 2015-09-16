"""Tasky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from Tasky import settings

urlpatterns = i18n_patterns('',
                            url('', include('social.apps.django_app.urls', namespace='social')),
                            url(r'^admin/', include(admin.site.urls)),
                            url(r'^$', 'Tasky.views.index', name='homepage'),
                            url(r'^accounts/', include('registration.backends.default.urls')),
                            url(r'^markdown/', include('django_markdown.urls')),
                            url(r'^task/', include('task.urls', namespace='task')),
                            url(r'^comments/', include('comments.urls', namespace='comments')),
                            url(r'^user_account/', include('user_account.urls', namespace='user_account')),
                            url(r'^search/', include('haystack.urls')),
                            url(r'^ratings/', include('ratings.urls', namespace='ratings')),
                            )

urlpatterns += patterns(
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
