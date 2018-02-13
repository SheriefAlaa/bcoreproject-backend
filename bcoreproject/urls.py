from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/risktype/', include('bcoreproject.api.urls', namespace='api-risktypes')),
]
