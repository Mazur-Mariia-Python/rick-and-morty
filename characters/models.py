from django.db import models


class Character(models.Model):
    class StatusChoices(models.TextChoices):
        ALIVE = "Alive"
        DEAD = "Dead"
        UNKNOWN = "unknown"

    # Female', 'Male', 'Genderless' or 'unknown'
    class GenderChoices(models.TextChoices):
        FEMALE = "Female"
        MALE = "Male"
        GENDERLESS = "Genderless"
        UNKNOWN = "unknown"

    """api_id - the id of the character from "https://rickandmortyapi.com/api/character"""
    api_id = models.IntegerField(unique=True)
    # name	string	The name of the character.
    name = models.CharField(max_length=255)
    # status	string	The status of the character ('Alive', 'Dead' or 'unknown').
    status = models.CharField(max_length=50, choices=StatusChoices.choices)
    # species	string	The species of the character.
    species = models.CharField(max_length=255)
    # gender	string	The gender of the character ('Female', 'Male', 'Genderless' or 'unknown').
    gender = models.CharField(max_length=50, choices=GenderChoices.choices)
    # image	string (url)	Link to the character's image. All images are 300x300px
    # and most are medium shots or portraits since they are intended to be used as avatars.
    image = models.URLField(max_length=255, unique=True)

    def __str__(self):
        return self.name
