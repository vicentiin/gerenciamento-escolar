"""
Configuração da interface de administração do Django para turmas, disciplinas e faltas.

Registra os modelos principais do aplicativo de turmas na interface administrativa
do Django Admin com customizações de display e métodos para exibição de dados relacionados.
"""

from django.contrib import admin  # type: ignore
from .models import Turma, Disciplina, Turma_Disciplina, Falta

# Register your models here.


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    """
    Interface de administração para turmas.

    Funcionalidades:
    - Visualização com informações de alunos associados
    - Busca por número e sala
    - Filtro por status (ativa/inativa)
    - Ordenação por número

    Métodos customizados:
    - nome_aluno(): Exibe os 5 primeiros alunos da turma
    - quantidade_alunos(): Exibe total de alunos
    """
    list_display = ('numero', 'sala', 'quantidade_maxima',
                    'status', 'update_at', 'nome_aluno', 'quantidade_alunos')
    search_fields = ('numero', 'sala',)
    list_filter = ('status',)
    ordering = ('numero',)

    def nome_aluno(self, obj):
        alunos = obj.alunos.all()[:5]
        return ", ".join([aluno.nome for aluno in alunos]) + ("..." if obj.alunos.count() > 5 else "")
    nome_aluno.short_description = 'Aluno'

    def quantidade_alunos(self, obj):
        return obj.alunos.count()
    quantidade_alunos.short_description = 'Quantidade de alunos'


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    """
    Interface de administração para disciplinas.

    Funcionalidades:
    - Busca por nome da disciplina
    """
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Turma_Disciplina)
class TurmaDisciplinaAdmin(admin.ModelAdmin):
    """
    Interface de administração para vinculações turma-disciplina.

    Funcionalidades:
    - Visualização com número da turma e nome da disciplina customizados
    - Busca por número da turma
    - Filtro por status da turma

    Métodos customizados:
    - numero_turma(): Exibe o número da turma relacionada
    - nome_disciplina(): Exibe o nome da disciplina relacionada
    - status_turma(): Exibe o status da turma
    """
    list_display = ('numero_turma', 'nome_disciplina')
    search_fields = ('turma__numero',)
    list_filter = ('turma__status',)

    def numero_turma(self, obj):
        return obj.turma.numero
    numero_turma.short_description = 'Turma'

    def nome_disciplina(self, obj):
        return obj.disciplina.nome
    nome_disciplina.short_description = 'Disciplina'

    def status_turma(self, obj):
        return obj.turma.status
    status_turma.short_description = 'Status da Turma'


@admin.register(Falta)
class FaltaAdmin(admin.ModelAdmin):
    """
    Interface de administração para registros de faltas.

    Funcionalidades:
    - Visualização com informações do aluno, disciplina, turma e status formatado
    - Busca por nome do aluno e data
    - Filtro por status do aluno

    Métodos customizados:
    - nome_aluno(): Exibe o nome do aluno
    - nome_disciplina(): Exibe o nome da disciplina
    - turma_disciplina(): Exibe o número da turma
    - status_aluno(): Exibe o status do aluno
    - status_formatado(): Converte status booleano em "Falta" ou "Presente"
    """
    list_display = ('nome_aluno', 'nome_disciplina',
                    'turma_disciplina', 'data', 'status_formatado', 'update_at')
    search_fields = ('aluno__nome', 'data',)
    list_filter = ('aluno__status',)

    def nome_aluno(self, obj):
        return obj.aluno.nome
    nome_aluno.short_description = 'Aluno'

    def nome_disciplina(self, obj):
        if obj.turma_disciplina.disciplina:
            return obj.turma_disciplina.disciplina.nome
        return "sem disciplina associada"
    nome_disciplina.short_description = 'Disciplina'

    def turma_disciplina(self, obj):
        if obj.turma_disciplina.turma:
            return obj.turma_disciplina.turma.numero
        return "sem turma associda"
    turma_disciplina.short_description = 'Turma'

    def status_aluno(self, obj):
        return obj.aluno.status
    status_aluno.short_description = 'Status do Aluno'

    def status_formatado(self, obj):
        return 'Falta' if obj.status else 'Presente'
    status_formatado.short_description = 'Status'
