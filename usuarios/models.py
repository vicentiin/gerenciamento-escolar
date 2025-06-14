from django.db import models #type: ignore
from django.contrib.auth.models import User
# Create your models here.

class SegmentoChoices(models.IntegerChoices):
    INFANTIL = 1, 'Educação Infantil'
    FUNDAMENTAL = 2, 'Ensino Fundamental'
    SEM_SEGMENTO = 0, 'Sem segmento'

class Pessoa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=70, null = False, verbose_name='Nome')
    cpf = models.CharField(max_length=14, null = False, verbose_name='CPF')
    data_nascimento = models.DateField(null = False, verbose_name='Data de nascimento')
    status = models.BooleanField(default=True, verbose_name='Ativo')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True


class Aluno(Pessoa):
    matricula = models.AutoField(primary_key=True)
    turma = models.ForeignKey('turmas.Turma', on_delete=models.RESTRICT, related_name='alunos', null=True, blank=True)
    senha = senha = models.CharField(max_length=128, null=False, verbose_name='Senha', default="aluno123")
    
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        return f"{self.matricula} - {self.nome}"

class Coordenador(Pessoa):
    matricula = models.AutoField(primary_key=True)
    email = models.CharField(max_length=120, verbose_name='E-mail', default='fulano@gmail.com')
    senha = models.CharField(max_length=128, null=False, verbose_name='Senha')
    segmento = models.IntegerField(choices=SegmentoChoices.choices, default=SegmentoChoices.SEM_SEGMENTO)
    turma = models.ForeignKey('turmas.Turma', on_delete=models.RESTRICT, verbose_name='Turma',related_name='coordenador_turma', null=True)
    

    class Meta:
        ordering = ['nome','segmento'] #type: ignore
        verbose_name = 'Coordenador'
        verbose_name_plural = 'Coordenadores'

    def __str__(self):
        return f"{self.matricula} - {self.nome} - {self.get_segmento_display()}"
    

class Professor(Pessoa):
    matricula = models.AutoField(primary_key=True)
    email = models.CharField(max_length=120, verbose_name='E-mail', default='fulano@gmail.com')
    senha = models.CharField(max_length=128, null=False, verbose_name='Senha')
    segmento = models.IntegerField(choices=SegmentoChoices.choices, default=SegmentoChoices.SEM_SEGMENTO, verbose_name='Segmento')


    class Meta:
        ordering = ['nome','segmento'] #type: ignore
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return f"{self.matricula} - {self.nome} - {self.get_segmento_display()}"
    


