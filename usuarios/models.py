"""
Definição de Modelos de Usuários para o Sistema de Gestão Escolar.

Este arquivo contém os modelos de dados (ORM Django) para representar os usuários
do sistema. Implementa diferentes tipos de usuários com suas características específicas:

Modelos:
- SegmentoChoices: Enumeração dos segmentos de ensino (Infantil, Fundamental, Sem segmento)
- Pessoa: Classe abstrata com dados comuns a todos os usuários
- Aluno: Modelo para alunos da escola
- Coordenador: Modelo para coordenadores pedagógicos
- Professor: Modelo para professores

Características gerais:
- Todos os usuários herdam de Pessoa (herança por abstração)
- Cada usuário está associado a um usuário Django (User) para autenticação
- Rastreamento de criação e atualização de registros
- Controle de ativação/desativação de usuários
"""

from django.db import models  # type: ignore
from django.contrib.auth.models import User
# Create your models here.


class SegmentoChoices(models.IntegerChoices):
    """
    Enumeração dos segmentos de ensino suportados pelo sistema.

    Valores:
    - INFANTIL (1): Educação Infantil
    - FUNDAMENTAL (2): Ensino Fundamental
    - SEM_SEGMENTO (0): Sem segmento especificado
    """
    INFANTIL = 1, 'Educação Infantil'
    FUNDAMENTAL = 2, 'Ensino Fundamental'
    SEM_SEGMENTO = 0, 'Sem segmento'


class Pessoa(models.Model):
    """
    Modelo abstrato que define os dados comuns a todos os usuários do sistema.

    Atributos:
    - user: Relação one-to-one com o modelo User do Django (para autenticação)
    - nome: Nome completo da pessoa (máx. 70 caracteres)
    - cpf: CPF da pessoa (máx. 14 caracteres - formato 000.000.000-00)
    - data_nascimento: Data de nascimento
    - status: Indicador de ativação do usuário (padrão: True)
    - create_at: Data e hora de criação do registro (automática)
    - update_at: Data e hora da última atualização (automática)

    Esta classe não pode ser instanciada diretamente, serve como base para
    Aluno, Coordenador e Professor.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=70, null=False, verbose_name='Nome')
    cpf = models.CharField(max_length=14, null=False, verbose_name='CPF')
    data_nascimento = models.DateField(
        null=False, verbose_name='Data de nascimento')
    status = models.BooleanField(default=True, verbose_name='Ativo')
    create_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True


class Aluno(Pessoa):
    """
    Modelo para representar alunos da instituição.

    Atributos:
    - matricula: Número de matrícula único do aluno (chave primária, auto-incrementado)
    - turma: Relação com a turma do aluno (ForeignKey para turmas.Turma)
    - senha: Senha do aluno (padrão: 'aluno123')

    Comportamento:
    - Ordenação por nome
    - Representação em string: "Matrícula - Nome"
    """
    matricula = models.AutoField(primary_key=True)
    turma = models.ForeignKey('turmas.Turma', on_delete=models.RESTRICT,
                              related_name='alunos', null=True, blank=True)
    senha = senha = models.CharField(
        max_length=128, null=False, verbose_name='Senha', default="aluno123")

    class Meta:
        ordering = ['nome']
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        return f"{self.matricula} - {self.nome}"


class Coordenador(Pessoa):
    """
    Modelo para representar coordenadores pedagógicos.

    Atributos:
    - matricula: Número de matrícula único do coordenador (auto-incrementado)
    - email: Endereço de e-mail do coordenador
    - senha: Senha do coordenador
    - segmento: Segmento de ensino sob sua coordenação (INT, FUND ou SEM_SEGMENTO)
    - turma: Relação com a turma coordenada (ForeignKey para turmas.Turma)

    Comportamento:
    - Ordenação por nome e segmento
    - Representação em string: "Matrícula - Nome - Segmento"
    """
    matricula = models.AutoField(primary_key=True)
    email = models.CharField(
        max_length=120, verbose_name='E-mail', default='fulano@gmail.com')
    senha = models.CharField(max_length=128, null=False, verbose_name='Senha')
    segmento = models.IntegerField(
        choices=SegmentoChoices.choices, default=SegmentoChoices.SEM_SEGMENTO)
    turma = models.ForeignKey('turmas.Turma', on_delete=models.RESTRICT,
                              verbose_name='Turma', related_name='coordenador_turma', null=True)

    class Meta:
        ordering = ['nome', 'segmento']  # type: ignore
        verbose_name = 'Coordenador'
        verbose_name_plural = 'Coordenadores'

    def __str__(self):
        return f"{self.matricula} - {self.nome} - {self.get_segmento_display()}"


class Professor(Pessoa):
    """
    Modelo para representar professores da instituição.

    Atributos:
    - matricula: Número de matrícula único do professor (auto-incrementado)
    - email: Endereço de e-mail do professor
    - senha: Senha do professor
    - segmento: Segmento de ensino que leciona (INT, FUND ou SEM_SEGMENTO)

    Comportamento:
    - Ordenação por nome e segmento
    - Representação em string: "Matrícula - Nome - Segmento"
    """
    matricula = models.AutoField(primary_key=True)
    email = models.CharField(
        max_length=120, verbose_name='E-mail', default='fulano@gmail.com')
    senha = models.CharField(max_length=128, null=False, verbose_name='Senha')
    segmento = models.IntegerField(choices=SegmentoChoices.choices,
                                   default=SegmentoChoices.SEM_SEGMENTO, verbose_name='Segmento')

    class Meta:
        ordering = ['nome', 'segmento']  # type: ignore
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return f"{self.matricula} - {self.nome} - {self.get_segmento_display()}"
