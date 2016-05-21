from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
    def __str__(self):
        return self.name

class Tema(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    class Meta:
        verbose_name = 'Тему'
        verbose_name_plural = 'Темы'
    def __str__(self):
        return self.name

class Vajnost(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    class Meta:
        verbose_name = 'Важность'
        verbose_name_plural = 'Важность'
    def __str__(self):
        return self.name

class Otdel(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
    def __str__(self):
        return self.name

class Tip(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
    def __str__(self):
        return self.name



class User(AbstractUser):
    otdel = models.ForeignKey(Otdel,blank=True,null=True)

class SupportRecuest(models.Model):
    creator = models.ForeignKey(User)
    date = models.DateField()
    type = models.ForeignKey(Tip)
    vajnost = models.ForeignKey(Vajnost)
    status = models.ForeignKey(Status)
    srok = models.DateField()
    tema = models.ForeignKey(Tema)
    desc = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = 'Заявку'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return "Заявка#%d" % self.id

class Message(models.Model):
    support_rec = models.ForeignKey(SupportRecuest)
    user = models.ForeignKey(User)
    text = models.TextField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return "Сообщение#%d" % self.id

class Spec(models.Model):
    support_rec = models.ForeignKey(SupportRecuest, unique=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return "Специалист#%d" % self.id