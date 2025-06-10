from django.urls import path 
from .views import (
    cadastro_avaliacao,
    cadastro_nota,
)


urlpatterns = [
    path('cadastro-avaliacao/', cadastro_avaliacao, name="cadastro_avaliacao"),
    path('cadastro-nota/', cadastro_nota, name="cadastro_nota")
]
