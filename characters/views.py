import random

from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Character
from .serializers import CharacterSerializer


@api_view(["GET"])
def get_random_character_view(request: Request) -> Response:
    pks = Character.objects.values_list("pk", flat=True)
    random_pk = random.choice(pks)
    random_character = Character.objects.get(pk=random_pk)
    serializer = CharacterSerializer(random_character)
    return Response(serializer.data, status=status.HTTP_200_OK)


# class PurchaseList(generics.ListAPIView):
#     serializer_class = PurchaseSerializer
#
#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = Purchase.objects.all()
#         username = self.request.query_params.get('username')
#         if username is not None:
#             queryset = queryset.filter(purchaser__username=username)
#         return queryset


class CharacterListView(generics.ListAPIView):
    serializer_class = CharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.all()

        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
            # queryset = queryset.filter(name__contains=name)
            # queryset = queryset.filter(name=name)
        return queryset
