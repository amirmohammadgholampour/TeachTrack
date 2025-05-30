# Generated by Django 5.2.1 on 2025-05-10 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classroom', '0001_initial'),
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_value', models.FloatField(max_length=20, verbose_name='Score')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score_classroom', to='classroom.classroom')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score_lesson', to='lesson.lesson')),
            ],
        ),
    ]
