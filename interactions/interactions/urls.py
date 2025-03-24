from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
]

#Add URL maps to redirect the base URL to our application
urlpatterns += [
    path('interactions/', include('interactionsapp.urls')),
]

