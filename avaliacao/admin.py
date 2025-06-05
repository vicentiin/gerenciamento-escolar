from django.contrib import admin #type:ignore
from .models import Avaliacao, Nota

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'arquivo', 'status', 'disciplina', 'turmas', 'data_aplicacao', 'periodo_letivo')
    search_fields = ('titulo', 'turma_disciplina__disciplina__nome', 'data_aplicacao', )
    list_filter = ('status',)
    filter_horizontal = ('turma_disciplina',)

    def disciplina(self, obj):
        disciplinas = obj.turma_disciplina.all()
        if disciplinas.count() > 0:
            return ", ".join([turma_disciplina.disciplina.nome for turma_disciplina in disciplinas])
        else:
            return ""
    disciplina.short_description = 'Disciplina'

    def turmas(self, obj):
        turmas = obj.turma_disciplina.all()
        if turmas.count() > 0:
            return ", ".join([turma_disciplina.turma.numero for turma_disciplina in turmas])
        else:
            return ""
    turmas.short_description = 'Turmas'


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('nome_aluno', 'titulo_avaliacao', 'pontuacao', 'relevancia')
    search_fields = ('aluno__nome',)
    list_filter = ('aluno',)

    def nome_aluno(self, obj):
        return obj.aluno.nome
    nome_aluno.short_description = 'Aluno'

    def titulo_avaliacao(self, obj):
        return obj.avaliacao.titulo
    titulo_avaliacao.short_description = 'Avaliação'
    


