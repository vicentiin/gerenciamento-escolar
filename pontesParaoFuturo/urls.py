"""
Configuração principal de URLs do projeto pontesParaoFuturo.

Define as rotas raiz da aplicação, incluindo a página inicial, painel de admin
e as rotas dos aplicativos (usuarios, turmas, avaliacao).

Estructura de rotas:
- /: Página inicial
- /admin/: Painel de administração do Django
- /auth/: Rotas de usuários (login, cadastros, painéis)
- /auth-turmas/: Rotas de turmas e disciplinas
- /auth-avaliacao/: Rotas de avaliações e notas

Media files:
- Configurado para servir arquivos de mídia (uploads) em desenvolvimento
"""

from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore
from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore
from .views import (
    pagina_inicial,
)


# Define os padrões de URL principais
urlpatterns = [
    path('', pagina_inicial, name="pagina_inicial"),
    path('admin/', admin.site.urls),
    path('auth/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('auth-turmas/', include(('turmas.urls', 'turmas'), namespace='turmas')),
    path('auth-avaliacao/',
         include(('avaliacao.urls', 'avaliacao'), namespace='avaliacao'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
