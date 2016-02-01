from django.conf.urls import include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView

class NewRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/'

urlpatterns = [
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls', namespace="rango")),
    url(r'^accounts/register/$', NewRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls'))
]
