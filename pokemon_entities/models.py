from django.db import models  # noqa F401


class Pokemon(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='предок',
        )
    title = models.CharField('имя', max_length=200)
    title_en = models.CharField('имя на английском', max_length=200, blank=True)
    title_jp = models.CharField('имя на японском', max_length=200, blank=True)
    description = models.TextField('описание', blank=True)
    img = models.ImageField('картинка', upload_to='img', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='покемон',
        )
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    appeared_at = models.DateTimeField('время появления', null=True, blank=True,)
    disappeared_at = models.DateTimeField('время исчезновения', null=True, blank=True,)
    level = models.IntegerField('уровень', null=True, blank=True,)
    health = models.IntegerField('здоровье', null=True, blank=True,)
    strength = models.IntegerField('сила', null=True, blank=True,)
    defence = models.IntegerField('защита', null=True, blank=True,)
    stamina = models.IntegerField('выносливость', null=True, blank=True)
