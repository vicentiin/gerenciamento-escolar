"""
Configuração de URLs do aplicativo de Usuários (Usuarios).

Este arquivo define as rotas de URL para as funcionalidades de:
- Autenticação e login de usuários
- Cadastro de diferentes tipos de usuários (Admin, Professor, Coordenador, Aluno)
- Exibição dos painéis personalizados para cada tipo de usuário

Padrão de URL: /auth/usuarios/<rota>

Rotas de Cadastro:
- /auth/usuarios/cadastro-admin/ - Cadastro de administrador
- /auth/usuarios/cadastro-professor/ - Cadastro de professor
- /auth/usuarios/cadastro-coordenador/ - Cadastro de coordenador
- /auth/usuarios/cadastro-aluno/ - Cadastro de aluno

Rotas de Autenticação:
- /auth/usuarios/login/ - Login de usuários

Rotas de Painéis:
- /auth/usuarios/tela-admin/ - Painel do administrador
- /auth/usuarios/tela-professor/ - Painel do professor
- /auth/usuarios/tela-coordenador/ - Painel do coordenador
"""

from django.urls import path  # type: ignore
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

# Define os padrões de URL para o aplicativo de usuários
urlpatterns = [
    # Rotas de cadastro de usuários
    path('cadastro-professor/', cadastro_professor, name="cadastro_professor"),
    path('cadastro-coordenador/', cadastro_coordenador,
         name="cadastro_coordenador"),
    path('cadastro-aluno/', cadastro_aluno, name="cadastro_aluno"),
    path('cadastro-admin/', cadastro_admin, name="cadastro_admin"),

    # Rota de autenticação
    path('login/', login, name="login"),

    # Rotas dos painéis de usuários
    path('tela-admin/', tela_admin, name="tela_admin"),
    path('tela-professor/', tela_professor, name="tela_professor"),
    path('tela-coordenador/', tela_coordenador, name="tela_coordenador")
]
