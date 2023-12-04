from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from characters.views import get_random_character_view, CharacterListView

urlpatterns = [
    path("characters/random/", get_random_character_view, name="character-random"),
    # use router only for ViewSet.
    path("characters/", CharacterListView.as_view(), name="character-list"),
]

app_name = "characters"
