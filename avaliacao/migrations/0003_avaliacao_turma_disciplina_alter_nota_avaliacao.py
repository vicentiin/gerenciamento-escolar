# Generated by Django 5.1.7 on 2025-05-04 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avaliacao', '0002_rename_avalicao_avaliacao'),
        ('turmas', '0005_alter_falta_aluno_alter_turma_disciplina_disciplina_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='turma_disciplina',
            field=models.ManyToManyField(related_name='avaliacao_turma_disciplina', to='turmas.turma_disciplina', verbose_name='Turma e Disciplina'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='avaliacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nota_avaliacao', to='avaliacao.avaliacao'),
        ),
    ]
