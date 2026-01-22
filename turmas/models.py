"""
Definição de Modelos para Gerenciamento de Turmas, Disciplinas e Faltas.

Este arquivo contém os modelos de dados (ORM Django) para representar as estruturas
acadêmicas do sistema:

Modelos:
- Turma: Representa as turmas/classes da escola
- Disciplina: Representa as disciplinas/matérias oferecidas
- Turma_Disciplina: Vinculação entre turmas e disciplinas com alocação de professores
- Falta: Registro de faltas/presenças de alunos
"""

from django.db import models  # type: ignore


# Create your models here.
class Turma(models.Model):
    """
    Modelo que representa uma turma/classe da escola.

    Atributos:
    - numero: Identificação da turma (ex: "1A", "2B")
    - sala: Número da sala de aula
    - quantidade_maxima: Limite de alunos na turma
    - status: Indicador se a turma está ativa ou inativa
    - update_at: Data e hora da última atualização

    Comportamento:
    - Ordenação por número e sala
    - Representação em string: "Número - Sala - Status"
    """
    numero = models.CharField(max_length=3, null=False, verbose_name='Numero')
    sala = models.CharField(max_length=3, null=False,
                            verbose_name='Numero da sala')
    quantidade_maxima = models.IntegerField(
        null=False, verbose_name='Quantidade máxima de alunos')
    status = models.BooleanField(default=True, verbose_name='Ativa')
    update_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering: ['numero', 'sala']  # type: ignore
        verbose_name: 'Turma'
        verbose_name_plural = 'Turmas'

    def __str__(self):
        return f"{self.numero} - {self.sala} - {'Ativa' if self.status else 'Inativa'}"


class Disciplina(models.Model):
    """
    Modelo que representa uma disciplina/matéria.

    Atributos:
    - nome: Nome da disciplina (ex: "Matemática", "Português")

    Comportamento:
    - Ordenação por nome
    - Representação em string: nome da disciplina
    """
    nome = models.CharField(null=False, max_length=30, verbose_name='Nome')

    class Meta:
        ordering = ['nome']  # type: ignore
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def __str__(self):
        return self.nome


class Turma_Disciplina(models.Model):
    """
    Modelo de junção que vincula disciplinas a turmas e aloca professores.

    Atributos:
    - turma: Relação com a turma (ForeignKey para Turma)
    - disciplina: Relação com a disciplina (ForeignKey para Disciplina)
    - professor: Relação com o professor responsável (ForeignKey para usuarios.Professor)

    Propósito:
    Permite que uma disciplina seja oferecida em múltiplas turmas com diferentes
    professores, e que uma turma tenha múltiplas disciplinas.

    Comportamento:
    - Ordenação por turma
    - Representação em string: "Número da Turma - Nome da Disciplina"
    """
    turma = models.ForeignKey(
        Turma, on_delete=models.RESTRICT, related_name='turma_disciplina')
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.RESTRICT, related_name='disciplina_turma')
    professor = models.ForeignKey("usuarios.Professor", verbose_name="Professor",
                                  on_delete=models.RESTRICT, null=True, related_name="prof_turma_disciplina")

    class Meta:
        ordering = ['turma']
        verbose_name = 'Turma Disciplina'
        verbose_name_plural = 'Turmas Disciplinas'

    def __str__(self):
        return f"{self.turma.numero} - {self.disciplina.nome}"


class Falta(models.Model):
    """
    Modelo que registra faltas/presenças de alunos em disciplinas.

    Atributos:
    - aluno: Relação com o aluno (ForeignKey para usuarios.Aluno)
    - turma_disciplina: Relação com turma-disciplina (ForeignKey para Turma_Disciplina)
    - data: Data do registro (preenchida automaticamente com data atual)
    - status: True para falta, False para presença
    - update_at: Data e hora da última atualização

    Comportamento:
    - Ordenação por data
    - Representação em string: "Nome do Aluno - Disciplina - Data = Status"
    """
    aluno = models.ForeignKey(
        'usuarios.Aluno', on_delete=models.CASCADE, related_name='falta_aluno')
    turma_disciplina = models.ForeignKey(
        Turma_Disciplina, on_delete=models.RESTRICT, related_name='faltas', null=True)
    data = models.DateField(auto_now_add=True, null=False, verbose_name='Data')
    status = models.BooleanField(default=True, verbose_name='Falta')
    update_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering: ['data']  # type: ignore
        verbose_name: 'Falta'
        verbose_name_plural = 'Faltas'

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma_disciplina.disciplina.nome} - {self.data} = {'Falta' if self.status else 'Presente'}"
