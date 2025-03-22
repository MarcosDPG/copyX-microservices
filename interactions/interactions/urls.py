from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
]

#Add URL maps to redirect the base URL to our application
urlpatterns += [
    path('', RedirectView.as_view(url='/interactions/', permanent=True)),
]

