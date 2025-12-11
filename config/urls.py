from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui as rotas do app Core na raiz do site
    path('', include('core.urls')),
    # Vamos precisar das rotas de autenticação também (login/logout)
    path('accounts/', include('django.contrib.auth.urls')),
]