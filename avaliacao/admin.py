"""
Configuração da interface de administração do Django para avaliações e notas.

Registra os modelos de avaliações e notas na interface administrativa do Django Admin
com customizações de display, filtros e métodos para exibição de dados relacionados.
"""

from django.contrib import admin  # type:ignore
from .models import Avaliacao, Nota


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    """
    Interface de administração para avaliações.

    Funcionalidades:
    - Visualização com disciplinas e turmas customizadas
    - Busca por título, nome da disciplina e data de aplicação
    - Filtro por status (Aplicada, Não aplicada, Corrigida)
    - Seletor horizontal para turmas-disciplinas

    Métodos customizados:
    - disciplina(): Exibe as disciplinas vinculadas à avaliação
    - turmas(): Exibe as turmas onde a avaliação será/foi aplicada
    """
    list_display = ('titulo', 'descricao', 'arquivo', 'status',
                    'disciplina', 'turmas', 'data_aplicacao', 'periodo_letivo')
    search_fields = (
        'titulo', 'turma_disciplina__disciplina__nome', 'data_aplicacao', )
    list_filter = ('status',)
    filter_horizontal = ('turma_disciplina',)

    def disciplina(self, obj):
        """Retorna as disciplinas vinculadas à avaliação ou string vazia se nenhuma."""
        disciplinas = obj.turma_disciplina.all()
        if disciplinas.count() > 0:
            return ", ".join([turma_disciplina.disciplina.nome for turma_disciplina in disciplinas])
        else:
            return ""
    disciplina.short_description = 'Disciplina'

    def turmas(self, obj):
        """Retorna as turmas onde a avaliação está vinculada ou string vazia se nenhuma."""
        turmas = obj.turma_disciplina.all()
        if turmas.count() > 0:
            return ", ".join([turma_disciplina.turma.numero for turma_disciplina in turmas])
        else:
            return ""
    turmas.short_description = 'Turmas'


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    """
    Interface de administração para notas.

    Funcionalidades:
    - Visualização com nome do aluno e título da avaliação customizados
    - Busca por nome do aluno
    - Filtro por aluno

    Métodos customizados:
    - nome_aluno(): Exibe o nome do aluno
    - titulo_avaliacao(): Exibe o título da avaliação
    """
    list_display = ('nome_aluno', 'titulo_avaliacao',
                    'pontuacao', 'relevancia')
    search_fields = ('aluno__nome',)
    list_filter = ('aluno',)

    def nome_aluno(self, obj):
        """Retorna o nome do aluno."""
        return obj.aluno.nome
    nome_aluno.short_description = 'Aluno'

    def titulo_avaliacao(self, obj):
        """Retorna o título da avaliação."""
        return obj.avaliacao.titulo
    titulo_avaliacao.short_description = 'Avaliação'
