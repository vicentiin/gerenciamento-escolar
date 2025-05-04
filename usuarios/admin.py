from django.contrib import admin #type: ignore
from .models import Aluno, Professor, Coordenador
# Register your models here.

@admin.register(Aluno)
class AlunosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento', 'numero_turma', 'status', 'create_at', 'update_at')
    search_fields = ('matricula', 'nome', 'cpf', 'data_nascimento',)
    list_filter = ('status',)

    def numero_turma(self, obj):
        return obj.turma.numero
    numero_turma.short_descreption = 'Turma'

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento', 'segmento', 'turma', 'disciplina', 'status', 'create_at', 'update_at')
    search_fields = ('matricula', 'nome', 'cpf', 'segmento',)
    list_filter = ('status',)

    def turma(self, obj):
        turmas = obj.turma_disciplina.all()
        if turmas.count() > 0:
            return ", ".join([turma_disciplina.turma.numero for turma_disciplina in turmas])
        else:
            ""
    turma.short_description = 'Turmas'

    def disciplina(self, obj):
        return obj.turma_disciplina.disciplina.nome
    disciplina.short_description = 'Disciplina'

@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento','turma', 'segmento', 'status', 'create_at', 'update_at')
    search_fields = ('matricula', 'nome', 'cpf', 'segmento',)
    list_filter = ('status',)

    def turma(self, obj):
        turmas = obj.turma.all()
        if turmas.count() > 0:
            return ", ".join([turma.numero for turma in turmas])
        else:
            return ""
    turma.short_description = 'Turmas'