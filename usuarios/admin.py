from django.contrib import admin #type: ignore
from .models import Aluno, Professor, Coordenador
# Register your models here.

@admin.register(Aluno)
class AlunosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento', 'status', 'create_at', 'update_at')
    search_fields = ('matricula', 'nome', 'cpf', 'data_nascimento',)
    list_filter = ('status',)

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento', 'senha', 'segmento', 'status', 'create_at', 'update_at')
    search_fields = ('matricula', 'nome', 'cpf', 'segmento',)
    list_filter = ('status',)

@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento', 'senha', 'segmento', 'status', 'create_at', 'update_at')
    search_fields = ('matricula', 'nome', 'cpf', 'segmento',)
    list_filter = ('status',)