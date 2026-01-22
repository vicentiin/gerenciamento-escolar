"""
Configuração de URLs do aplicativo de Turmas.

Este arquivo define as rotas de URL para as funcionalidades de:
- Cadastro de turmas
- Vinculação de disciplinas a turmas e alocação de professores
- Cadastro de disciplinas
- Registro de faltas de alunos

Padrão de URL: /turmas/<rota>
"""

from django.urls import path  # type: ignore
from .views import (
    cadastro_turma,
    cadastro_turmaDisciplina,
    cadastro_disciplina,
    cadastro_falta
)

# Define os padrões de URL para o aplicativo de turmas
urlpatterns = [
    path('cadastro-turma/', cadastro_turma, name="cadastro_turma"),
    path('cadastro-turmaDisciplina/', cadastro_turmaDisciplina,
         name="cadastro_turmaDisciplina"),
    path('cadastro-disciplina/', cadastro_disciplina, name="cadastro_disciplina"),
    path('cadastro-falta/', cadastro_falta, name="cadastro_falta")
]
