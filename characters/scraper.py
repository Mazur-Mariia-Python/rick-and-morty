from typing import List

import requests

from django.conf import settings
from django.db import IntegrityError

from .models import Character


def scrape_characters() -> List[Character]:
    next_url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL

    characters = []
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


def save_characters(characters: List[Character]) -> None:
    for character in characters:
        # Перевіряю чи персонаж, який хочу зберегти вже існує в БД чи ні.
        # Якщо існує, тоді викидаю повідомлення, що такий персонаж вже існує у БД.
        try:
            character.save()
        except IntegrityError:
            print(f"Character with 'api_id' {character.api_id} already exist in DB!")


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
