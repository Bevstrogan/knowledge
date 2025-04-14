from django.db import models
from django.db.models import ForeignKey

from users.models import User


class Breed(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название породы",
        help_text="Введите название породы",
    )
    description = models.TextField(
        verbose_name="Описание породы",
        help_text="Введите описание породы",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"

    def __str__(self):
        return self.name


class Dog(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Кличка собаки", help_text="Введите кличку собаки"
    )

    description = models.TextField(
        verbose_name="Описание собаки",
        help_text="Введите описание собаки",
        blank=True,
        null=True,
    )

    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Порода собаки",
        help_text="Введите породу собаки",
        related_name="dogs",
    )

    photo = models.ImageField(
        upload_to="dogs/photo",
        blank=True,
        null=True,
        verbose_name="Фото собаки",
        help_text="Загрузите фото собаки",
    )

    date_born = models.DateField(
        verbose_name="Дата рождения собаки",
        help_text="Введите дату рождения собаки",
        blank=True,
        null=True,
    )

    views_field = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите кол-во просмотров",
        default=0,
    )

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"
        ordering = ["breed", "name"]
        permissions = [
            ("can_edit_breed", "Cand edit breed"),
            ("can_edit_description", "Cand edit description")
        ]

    def __str__(self):
        return self.name


class Parent(models.Model):
    dog = ForeignKey(
        Dog,
        related_name="parents",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Собака",
    )
    name = models.CharField(
        max_length=100, verbose_name="Кличка собаки", help_text="Введите кличку собаки"
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Порода собаки",
        help_text="Введите породу собаки",
        related_name="parent_dogs",
    )
    year_born = models.PositiveIntegerField(
        verbose_name="Год рождения",
        help_text="Введите год рождения",
        default=0,
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца собаки",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Собака родитель"
        verbose_name_plural = "Собаки Родители"
        ordering = ["breed", "name"]

    def __str__(self):
        return self.name
