# Generated by Django 5.1.7 on 2025-05-20 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turmas', '0006_alter_falta_aluno_alter_falta_disciplina_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='quantidade_maxima',
            field=models.IntegerField(verbose_name='Quantidade máxima de alunos'),
        ),
    ]
