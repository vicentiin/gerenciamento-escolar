from django.urls import path #type: ignore
from .views import (
    cadastro_turma,
    cadastro_turmaDisciplina,
    cadastro_disciplina,
    cadastro_falta
)

urlpatterns = [
    path('cadastro-turma/', cadastro_turma, name="cadastro_turma"),
    path('cadastro-turmaDisciplina/', cadastro_turmaDisciplina, name="cadastro_turmaDisciplina"),
    path('cadastro-disciplina/', cadastro_disciplina, name="cadastro_disciplina"),
    path('cadastro-falta/', cadastro_falta, name="cadastro_falta")
]