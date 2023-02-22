from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('billapp.urls')),
    path('account/', include('accounts.urls')),
    path('<int:billing_slug>/groups/', include('groups.urls')),
    path('<int:billing_slug>/plans/', include('plans.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)