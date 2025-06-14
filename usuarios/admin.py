from django.contrib import admin #type: ignore
from .models import Aluno, Professor, Coordenador
import csv
from django.http import HttpResponse #type: ignore
# Register your models here.


@admin.register(Aluno)
class AlunosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento', 'numero_turma', 'status', 'create_at', 'update_at')
    search_fields = ('matricula', 'nome', 'cpf', 'data_nascimento',)
    list_filter = ('status',)

    def numero_turma(self, obj):
        if obj.turma:
            return obj.turma.numero
        return "Sem turma associada"
    numero_turma.short_description = 'Turma'

    def export_to_csv(self, request, queryset): 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = "alunos.csv"'
        writer = csv.writer(response)
        writer.writerow(['matricula', 'nome', 'cpf', 'data de nascimento', 'turma', 'status', 'criado em', 'atualizado em'])
        for aluno in queryset:
            writer.writerow([aluno.matricula, aluno.nome, aluno.cpf, aluno.data_nascimento, aluno.turma.numero, aluno.status, 
                             aluno.create_at, aluno.update_at]) 
        return response
    
    export_to_csv.short_description = 'Exportar para CSV'
    actions = [export_to_csv]

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento', 'segmento', 'turma', 'disciplina', 'status', 'create_at', 'update_at', 'senha')
    search_fields = ('matricula', 'nome', 'cpf', 'segmento',)
    list_filter = ('status',)

    def turma(self, obj):
        if obj.prof_turma_disciplina:
            turmas = obj.prof_turma_disciplina.all()
            return ", ".join([turma_disciplina.turma.numero for turma_disciplina in turmas])
        return "Professor ainda não alocado"
    turma.short_description = 'Turmas'

    def disciplina(self, obj):
        if obj.prof_turma_disciplina:
            disciplinas = obj.prof_turma_disciplina.all()
            return ", ".join([turma_disciplina.disciplina.nome for turma_disciplina in disciplinas])
        return "-"
    disciplina.short_description = 'Disciplina'

@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'data_nascimento','turma', 'segmento', 'senha', 'status', 'create_at', 'update_at')
    search_fields = ('matricula', 'nome', 'cpf', 'segmento',)
    list_filter = ('status',)

    def turma(self, obj):
        turmas = obj.turma.all()
        if turmas.count() > 0:
            return ", ".join([turma.numero for turma in turmas])
        else:
            return ""
    turma.short_description = 'Turmas'