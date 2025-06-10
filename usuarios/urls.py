from django.urls import path #type: ignore
from .views import (
    cadastro_professor,
    cadastro_coordenador,
    cadastro_aluno,
    cadastro_admin,
    login,
    tela_admin,
    tela_professor,
    tela_coordenador,
)

urlpatterns = [
    path('cadastro-professor/', cadastro_professor, name="cadastro_professor"),
    path('cadastro-coordenador/', cadastro_coordenador, name="cadastro_coordenador"),
    path('cadastro-aluno/', cadastro_aluno, name="cadastro_aluno"),
    path('cadastro-admin/', cadastro_admin, name="cadastro_admin"),
    path('login/', login, name="login"),

    path('tela-admin/', tela_admin, name="tela_admin"),
    path('tela-professor/', tela_professor, name="tela_professor"),
    path('tela-coordenador/', tela_coordenador, name="tela_coordenador")
]