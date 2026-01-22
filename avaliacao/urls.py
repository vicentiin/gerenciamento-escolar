"""
Configuração de URLs do aplicativo de Avaliações.

Este arquivo define as rotas de URL para as funcionalidades de:
- Cadastro de avaliações
- Registro de notas de alunos em avaliações

Padrão de URL: /avaliacao/<rota>
"""

from django.urls import path
from .views import (
    cadastro_avaliacao,
    cadastro_nota,
)


# Define os padrões de URL para o aplicativo de avaliações
urlpatterns = [
    path('cadastro-avaliacao/', cadastro_avaliacao, name="cadastro_avaliacao"),
    path('cadastro-nota/', cadastro_nota, name="cadastro_nota")
]
