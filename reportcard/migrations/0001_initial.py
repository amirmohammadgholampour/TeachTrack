# Generated by Django 5.2 on 2025-04-17 03:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classroom', '0001_initial'),
        ('score', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disciplinary_status', models.CharField(max_length=255)),
                ('grade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('class_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_cards', to='classroom.classroom')),
                ('scores', models.ManyToManyField(related_name='report_cards', to='score.score')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
