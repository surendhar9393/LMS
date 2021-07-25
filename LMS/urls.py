from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
import debug_toolbar
from LMS.user.views import index

from django.conf.urls.static import static
from django.conf import settings

# local imports
from LMS.user import views

urlpatterns = [
    url(r'^api/', include('LMS.lead.urls')),
    url(r'^api/', include('LMS.user.urls')),
    url('admin/', admin.site.urls),
    url(r'', index, name='index'),
    url(r'^__debug__/', include(debug_toolbar.urls)),

    # path(r'^')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
