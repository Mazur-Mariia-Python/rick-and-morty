from typing import List

import requests

from django.conf import settings

from characters.models import Character

# scrape_characters відповідає тільки за скрапінг інфо з певної api, щоб її дістати звідти
def scrape_characters() -> List[Character]:
    # don't use directly links
    # characters_response = requests.get("https://rickandmortyapi.com/api/character")

    next_url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL

    # Best practice. Краще зберігати посилання на сайт у settings.py
    # characters_response = requests.get(settings.RICK_AND_MORTY_API_CHARACTERS_URL).json()


    # return characters_response
    # Ми не зможемо запустити цю програмку, бо вона залежить від Django. Але її
    # можна запустити через Python Console. Це одночасно і Django Console, тому
    # є доступ до django.conf import settings і до модельок.
    characters = []
    # Логіка в тому, щоб ітеруватися доти поки next буде рівним null. Тоді зберемо інфо про всіх персонажів charactersз усіх сторінок
    while next_url_to_scrape is not None:
        characters_response = requests.get(next_url_to_scrape).json()

        for character_dict in characters_response["results"]:
            characters.append(
                Character(
                    api_id=character_dict["id"],
                    name=character_dict["name"],
                    status=character_dict["status"],
                    species=character_dict["species"],
                    gender=character_dict["gender"],
                    image=character_dict["image"],
                )
            )
        next_url_to_scrape = characters_response["info"]["next"]
    return characters


# функція для зберігання персонажів
def save_characters(characters: List[Character]) -> None:
    for character in characters:
        character.save()


# функція, яка спочатку скрапить персонажів з апіхи, а потів вже зберігає їх у БД
def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)

