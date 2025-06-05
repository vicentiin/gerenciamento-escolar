from django.urls import path 
from .views import (
    cadastro_avaliacao,
)


urlpatterns = [
    path('cadastro-avaliacao/', cadastro_avaliacao, name="cadastro_avaliacao"),
]
