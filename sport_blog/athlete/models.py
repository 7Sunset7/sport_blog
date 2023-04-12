from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Athlete(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    slug = models.SlugField(unique=True, verbose_name='URL')
    age = models.IntegerField(verbose_name='Возраст')
    content = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='athlete/', verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    sport = models.ForeignKey('AthleteSport', on_delete=models.PROTECT, verbose_name='Вид спорта', default='')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['updated_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class AthleteSport(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sport', kwargs={'sport_slug': self.slug})





