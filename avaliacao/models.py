"""
Definição de Modelos para Gerenciamento de Avaliações e Notas.

Este arquivo contém os modelos de dados (ORM Django) para representar as avaliações
e notas do sistema:

Enumerações:
- AvalicaoChoices: Estados possíveis de uma avaliação
- RelevanciaChoices: Níveis de relevância de uma nota
- PeriodoChoices: Períodos letivos (semestres)

Modelos:
- Avaliacao: Representa uma avaliação/prova aplicada em turmas-disciplinas
- Nota: Registro da pontuação de um aluno em uma avaliação
"""

from django.db import models  # type: ignore


class AvalicaoChoices(models.IntegerChoices):
    """
    Enumeração dos estados possíveis de uma avaliação.

    Valores:
    - APLICADA (1): Avaliação já foi aplicada aos alunos
    - NAO_APLICADA (2): Avaliação ainda não foi aplicada
    - CORRIGIDA (3): Avaliação foi corrigida
    """
    APLICADA = 1, 'Aplicada'
    NAO_APLICADA = 2, 'Não Aplicada'
    CORRIGIDA = 3, 'Corrigida'


class RelevanciaChoices(models.IntegerChoices):
    """
    Enumeração dos níveis de relevância de uma nota.

    Valores:
    - ALTA (1): Nota com alta relevância para o desempenho
    - MEDIA (2): Nota com média relevância
    - BAIXA (3): Nota com baixa relevância
    - NENHUMA (0): Nota sem relevância
    """
    ALTA = 1, 'Alta'
    MEDIA = 2, 'Media'
    BAIXA = 3, 'Baixa'
    NENHUMA = 0, 'Sem relevância'


class PeriodoChoices(models.IntegerChoices):
    """
    Enumeração dos períodos letivos do ano escolar.

    Valores:
    - SELECIONAR (0): Opção padrão (não selecionado)
    - PRIMEIRO (1): Primeiro semestre
    - SEGUNDO (2): Segundo semestre
    """
    SELECIONAR = 0, 'Selecione um período'
    PRIMEIRO = 1, 'Primeiro semestre'
    SEGUNDO = 2, 'Segundo semestre'


class Avaliacao(models.Model):
    """
    Modelo que representa uma avaliação/prova.

    Atributos:
    - titulo: Nome/título da avaliação
    - descricao: Descrição ou instruções da avaliação
    - arquivo: Arquivo anexado (ex: prova em PDF)
    - create_at: Data e hora de criação (automática)
    - status: Estado atual da avaliação (Aplicada, Não aplicada, Corrigida)
    - turma_disciplina: Relação muitos-para-muitos com turmas-disciplinas onde será aplicada
    - data_aplicacao: Data em que a avaliação foi/será aplicada
    - periodo_letivo: Semestre em que ocorre a avaliação

    Comportamento:
    - Ordenação por título
    - Representação em string: "Título - Status"
    """
    titulo = models.CharField(
        max_length=100, null=False, verbose_name='Titulo')
    descricao = models.TextField(verbose_name='Descrição')
    arquivo = models.FileField(upload_to='avaliacoes/', verbose_name='Arquivo')
    create_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em')
    status = models.IntegerField(choices=AvalicaoChoices.choices,
                                 default=AvalicaoChoices.NAO_APLICADA, verbose_name='Status')
    turma_disciplina = models.ManyToManyField(
        'turmas.Turma_Disciplina', verbose_name='Turma e Disciplina', related_name='avaliacao_turma_disciplina')
    data_aplicacao = models.DateField(null=True, verbose_name='Data')
    periodo_letivo = models.IntegerField(
        choices=PeriodoChoices.choices, default=PeriodoChoices.SELECIONAR, verbose_name='Período')

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"


class Nota(models.Model):
    """
    Modelo que representa a nota de um aluno em uma avaliação.

    Atributos:
    - aluno: Relação com o aluno (ForeignKey para usuarios.Aluno)
    - avaliacao: Relação com a avaliação (ForeignKey para Avaliacao)
    - pontuacao: Valor numérico da nota obtida pelo aluno
    - relevancia: Nível de relevância dessa nota para o desempenho geral (ALTA, MEDIA, BAIXA, NENHUMA)

    Comportamento:
    - Ordenação por pontuação
    - Representação em string: "Nome do Aluno - Título da Avaliação - Pontuação"
    """
    aluno = models.ForeignKey(
        'usuarios.Aluno', on_delete=models.CASCADE, related_name='nota_aluno')
    avaliacao = models.ForeignKey(
        Avaliacao, on_delete=models.CASCADE, related_name='nota_avaliacao')
    pontuacao = models.FloatField(verbose_name='Pontuação')
    relevancia = models.IntegerField(choices=RelevanciaChoices.choices,
                                     default=RelevanciaChoices.NENHUMA, verbose_name='Relevância', null=True)

    class Meta:
        ordering = ['pontuacao']
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return f"{self.aluno.nome} - {self.avaliacao.titulo} - {self.pontuacao}"
