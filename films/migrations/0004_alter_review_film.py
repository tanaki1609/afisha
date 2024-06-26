# Generated by Django 5.0.6 on 2024-05-21 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_alter_film_director_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='films.film'),
        ),
    ]
