# Generated by Django 5.1.7 on 2025-04-29 21:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0003_rename_updated_at_alunos_update_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Falta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('status', models.BooleanField(default=False, verbose_name='Falta')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='usuarios.alunos')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='turmas.disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(verbose_name='Numero')),
                ('sala', models.IntegerField(verbose_name='Numero da sala')),
                ('quantidadeMax', models.IntegerField(verbose_name='Qauntidade máxima de alunos')),
                ('status', models.BooleanField(default=True, verbose_name='Ativada')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('alunos', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='usuarios.alunos')),
            ],
        ),
        migrations.CreateModel(
            name='Turma_Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='turmas.disciplina')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='turmas.turma')),
            ],
        ),
    ]
