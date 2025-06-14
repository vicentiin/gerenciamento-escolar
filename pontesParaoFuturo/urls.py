"""
URL configuration for pontesParaoFuturo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin #type: ignore
from django.urls import path, include #type: ignore
from django.conf import settings #type: ignore
from django.conf.urls.static import static #type: ignore
from .views import (
    pagina_inicial,
)   


urlpatterns = [
    path('', pagina_inicial, name="pagina_inicial"),
    path('admin/', admin.site.urls),
    path('auth/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('auth-turmas/', include(('turmas.urls', 'turmas'), namespace='turmas')),
    path('auth-avaliacao/', include(('avaliacao.urls', 'avaliacao'), namespace='avaliacao'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
