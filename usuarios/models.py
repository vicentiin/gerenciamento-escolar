from django.db import models

# Create your models here.

class Alunos(models.Model):
    nome = models.CharField(max_length=70, null = False)
    cpf = models.CharField(max_length=14, null = False)
    data_nascimento = models.DateField(null = False)

    def __str__(self):
        return self.nome