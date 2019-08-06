"""learninglab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
# from django.conf.urls.static import static

# wagtail
# from wagtail.admin import urls as wagtailadmin_urls
# from wagtail.documents import urls as wagtaildocs_urls
# from wagtail.core import urls as wagtail_urls

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('courses/', include('courses.urls')),
    path('votes/', include('votes.urls')),
    path('homework/', include('homework.urls')),
    # wagtail
    # path('cms/', include(wagtailadmin_urls)),
    # path('documents/', include(wagtaildocs_urls)),
    # path('pages/', include(wagtail_urls)),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),

#     ]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
        serve, {'document_root':
            settings.MEDIA_ROOT, }), ]
