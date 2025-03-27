# Generated by Django 5.1.7 on 2025-03-26 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Breed",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название породы",
                        max_length=100,
                        verbose_name="Название породы",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Введите описание породы",
                        null=True,
                        verbose_name="Описание породы",
                    ),
                ),
            ],
            options={
                "verbose_name": "Порода",
                "verbose_name_plural": "Породы",
            },
        ),
        migrations.CreateModel(
            name="Dog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите кличку собаки",
                        max_length=100,
                        verbose_name="Кличка собаки",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите фото собаки",
                        null=True,
                        upload_to="dogs/photo",
                        verbose_name="Фото собаки",
                    ),
                ),
                (
                    "date_born",
                    models.DateField(
                        blank=True,
                        help_text="Введите дату рождения собаки",
                        null=True,
                        verbose_name="Дата рождения собаки",
                    ),
                ),
                (
                    "breed",
                    models.ForeignKey(
                        blank=True,
                        help_text="Введите породу собаки",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="dogs",
                        to="dogs.breed",
                        verbose_name="Порода собаки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Собака",
                "verbose_name_plural": "Собаки",
                "ordering": ["breed", "name"],
            },
        ),
    ]
