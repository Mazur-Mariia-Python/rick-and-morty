import random

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from pagination import CharactersListPagination
from .models import Character
from .serializers import CharacterSerializer


@extend_schema(responses={status.HTTP_200_OK: CharacterSerializer})
@api_view(["GET"])
def get_random_character_view(request: Request) -> Response:
    """Get random character from Rick & Morty world"""
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
    pagination_class = CharactersListPagination
    serializer_class = CharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.all()

        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
            # queryset = queryset.filter(name__contains=name)
            # queryset = queryset.filter(name=name)
        return queryset

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by name insensitive containts",
                required=False,
                type=str,
            ),
        ],
    )
    # перевизначаю метод get, бо саме він відповідає за метод characters list і
    # над ним написати @extend_schema
    def get(self, request, *args, **kwargs) -> Response:
        """List characters with filter by name"""
        return super().get(request, *args, **kwargs)

    # @extend_schema(
    #     # extra parameters added to the schema
    #     parameters=[
    #         OpenApiParameter(name='artist', description='Filter by artist',
    #         required=False, type=str),
    #         OpenApiParameter(
    #             name='release',
    #             type=OpenApiTypes.DATE,
    #             location=OpenApiParameter.QUERY,
    #             description='Filter by release date',
    #             examples=[
    #                 OpenApiExample(
    #                     'Example 1',
    #                     summary='short optional summary',
    #                     description='longer description',
    #                     value='1993-08-23'
    #                 ),
    #                 ...
    #             ],
    #         ),
    #     ],
    #     # override default docstring extraction
    #     description='More descriptive text',
    #     # provide Authentication class that deviates from the views default
    #     auth=None,
    #     # change the auto-generated operation name
    #     operation_id=None,
    #     # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
    #     operation=None,
    #     # attach request/response examples to the operation.
    #     examples=[
    #         OpenApiExample(
    #             'Example 1',
    #             description='longer description',
    #             value=...
    #         ),
    #         ...
    #     ],
    # )
    # def list(self, request):
    #     # your non-standard behaviour
    #     return super().list(request)
