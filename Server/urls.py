"""CCApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.i18n import JavaScriptCatalog
from User.token_operationsv2 import spend_token
from User.views import obtain_token, beartoken, verify_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Application.api.apiurls')),
    path('api/', include('Wizard.api.apiurls')),
    path('api/', include('AdminPanel.api.apiurls')),
    path('api/', include('Application3d.api.apiurls')),
    path('api/', include('agent.api.apiurls')),
    path('agent/', include('agent.urls')),
    path('token/.well-known/openid-configuration',  beartoken),
    path('api/token/', obtain_token),
    path('api/verifytoken/', verify_token),
    # path('o/token/', TokenView.as_view(), name='token'),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns += i18n_patterns(
    path('', include('Application.urls')),
    path('', include('Wizard.urls')),
    path('', include('Application3d.urls')),
    path('dashboard/', include('AdminPanel.urls')),
    path('', include('website.urls')),
    path(_('jsi18n/'), JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('rosetta/', include('rosetta.urls')),
    # prefix_default_language=False,
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)