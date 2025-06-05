from django.db import models #type: ignore

class AvalicaoChoices(models.IntegerChoices):
    APLICADA = 1, 'Aplicada'
    NAO_APLICADA = 2, 'Não Aplicada'
    CORRIGIDA = 3, 'Corrigida'

class RelevanciaChoices(models.IntegerChoices):
    ALTA = 1, 'Alta'
    MEDIA = 2, 'Media'
    BAIXA = 3, 'Baixa'
    NENHUMA = 0, 'Sem relevância'

class PeriodoChoices(models.IntegerChoices):
    SELECIONAR = 0, 'Selecione um período'
    PRIMEIRO = 1, 'Primeiro semestre'
    SEGUNDO = 2, 'Segundo semestre'

class Avaliacao(models.Model):
    titulo = models.CharField(max_length=100, null=False, verbose_name='Titulo')
    descricao = models.TextField(verbose_name='Descrição')
    arquivo = models.FileField(upload_to='avaliacoes/', verbose_name='Arquivo')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    status = models.IntegerField(choices=AvalicaoChoices.choices, default=AvalicaoChoices.NAO_APLICADA, verbose_name='Status')
    turma_disciplina = models.ManyToManyField('turmas.Turma_Disciplina', verbose_name='Turma e Disciplina', related_name='avaliacao_turma_disciplina')
    data_aplicacao = models.DateField(null=True, verbose_name='Data')
    periodo_letivo = models.IntegerField(choices=PeriodoChoices.choices, default=PeriodoChoices.SELECIONAR, verbose_name='Período')


    class Meta:
        ordering = ['titulo']
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
    
    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"
    

class Nota(models.Model):
    aluno = models.ForeignKey('usuarios.Aluno', on_delete=models.CASCADE, related_name='nota_aluno')
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='nota_avaliacao')
    pontuacao = models.FloatField(verbose_name='Pontuação')
    relevancia =models.IntegerField(choices=RelevanciaChoices.choices, default=RelevanciaChoices.NENHUMA, verbose_name='Relevância')

    class Meta:
        ordering = ['pontuacao']
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return f"{self.aluno.nome} - {self.avaliacao.titulo} - {self.pontuacao}"

