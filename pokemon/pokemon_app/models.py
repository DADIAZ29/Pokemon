from django.db import models

class PokemonSprites(models.Model):
    front_default = models.URLField(blank=True, null=True)
    back_default = models.URLField(blank=True, null=True)
    front_shiny = models.URLField(blank=True, null=True)
    back_shiny = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.front_default or "Sin imagen"


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    height = models.IntegerField()
    weight = models.IntegerField()
    order = models.IntegerField()
    sprites = models.ForeignKey(PokemonSprites, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
