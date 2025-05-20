from django.db import models #type: ignore

# Create your models here.
class Turma(models.Model):
    numero = models.CharField(max_length=3, null=False, verbose_name='Numero')
    sala = models.CharField(max_length=3, null=False, verbose_name='Numero da sala')
    quantidade_maxima = models.IntegerField(null=False, verbose_name='Quantidade máxima de alunos')
    status = models.BooleanField(default=True, verbose_name='Ativa')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering: ['numero','sala'] #type: ignore
        verbose_name: 'Turma'
        verbose_name_plural = 'Turmas'
    
    def __str__(self):
        return f"{self.numero} - {self.sala} - {'Ativa' if self.status else 'Inativa'}" 
    

class Disciplina(models.Model):
    nome = models.CharField(null=False, max_length=30, verbose_name='Nome')

    class Meta:
        ordering = ['nome'] #type: ignore
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def __str__(self):
        return self.nome
    

class Turma_Disciplina(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.RESTRICT, related_name='turma_disciplina')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.RESTRICT, related_name='disciplina_turma')

    class Meta:
        ordering = ['turma']
        verbose_name = 'Turma Disciplina'
        verbose_name_plural = 'Turmas Disciplinas'

    def __str__(self):
        return f"{self.turma.numero} - {self.disciplina.nome}"
    

class Falta(models.Model):
    aluno = models.ForeignKey('usuarios.Aluno', on_delete=models.CASCADE, related_name='falta_aluno')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='faltas')
    data = models.DateField(null=False, verbose_name='Data')
    status = models.BooleanField(default=False, verbose_name='Falta')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering: ['data'] #type: ignore
        verbose_name : 'Falta'
        verbose_name_plural = 'Faltas'

    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina.nome} - {self.data} = {'Falta' if self.status else 'Presente'}"
    


