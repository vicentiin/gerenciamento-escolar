from django.contrib import admin #type: ignore
from .models import Turma, Disciplina, Turma_Disciplina, Falta

# Register your models here.

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'sala', 'quantidade_maxima', 'status', 'update_at', 'nome_aluno', 'quantidade_alunos')
    search_fields = ('numero', 'sala',)
    list_filter = ('status',)
    ordering = ('numero',)

    def nome_aluno(self, obj):
        alunos = obj.alunos.all()[:5] #IRA EXIBIR OS 5 PRIMEIROS ALUNOS
        return ", ".join([aluno.nome for aluno in alunos]) + ("..." if obj.alunos.count() > 5 else "")
    nome_aluno.short_description = 'Aluno'

    def quantidade_alunos(self, obj):
        return obj.alunos.count()
    quantidade_alunos.short_description = 'Quantidade de alunos'

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Turma_Disciplina)
class TurmaDisciplinaAdmin(admin.ModelAdmin):
    list_display = ('numero_turma', 'nome_disciplina')
    search_fields = ('turma__numero',)
    list_filter = ('turma__status',)

    def numero_turma(self, obj):
        return obj.turma.numero #ACESSA O NOME DO OBJETO RELACIONADO
    numero_turma.short_description = 'Turma' #INFORMA A TABELA PARA SER ACESSADA NO ADMIN

    def nome_disciplina(self, obj):
        return obj.disciplina.nome #ACESSA O NOME DO OBJETO RELACIONADO
    nome_disciplina.short_description = 'Disciplina' #INFORMA A TABELA PARA SER ACESSADA NO ADMIN

    def status_turma(self, obj):
        return obj.turma.status #ACESSA O NOME DO OBJETO RELACIONADO
    status_turma.short_description = 'Status da Turma' #INFORMA A TABELA PARA SER ACESSADA NO ADMIN

@admin.register(Falta)
class FaltaAdmin(admin.ModelAdmin):
    list_display = ('nome_aluno', 'nome_disciplina', 'turma_disciplina', 'data', 'status_formatado', 'update_at')
    search_fields = ('aluno__nome', 'data',)
    list_filter = ('aluno__status',)

    def nome_aluno(self, obj):
        return obj.aluno.nome
    nome_aluno.short_description = 'Aluno'

    def nome_disciplina(self, obj):
        return obj.turma_disciplina.disciplina.nome
    nome_disciplina.short_description = 'Disciplina'

    def turma_disciplina(self, obj):
        return obj.turma_disciplina.turma.numero
    turma_disciplina.short_description = 'Turma'

    def status_aluno(self, obj):
        return obj.aluno.status
    status_aluno.short_description = 'Status do Aluno'

    def status_formatado(self, obj):
        return 'Falta' if obj.status else 'Presente'
    status_formatado.short_description = 'Status'
    
