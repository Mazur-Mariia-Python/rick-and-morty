# First task
# from characters.models import Character
#
# from celery import shared_task
#
#
# @shared_task
# def count_characters() -> int:
#     return Character.objects.count()


# Second task
from characters.scraper import sync_characters_with_api

from celery import shared_task


@shared_task
def run_sync_with_api() -> None:
    sync_characters_with_api()


# from celery import shared_task
#
#
# @shared_task
# def hello():
#     print("Hello there!")
