from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from skate_spots.models import Spot
from auth.api.serializers import UserBasicSerializer
from .serializers import UserSearchResultsSerializer

# from .serializers import (
#     DualLogInSerializer,
# )

User = get_user_model()


class SearchView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    allowed_methods = ("GET",)

    def get(self, request, format=None):
        """
        TODO IDEA:
        can only find people near you, to make point that it's for local connections.
        Make sure to tell people when asking to use location services.
        """
        data = {}
        initial_pagination = 25
        default_page = 1

        q = request.GET.get("search")
        page = request.GET.get("page", default_page)

        query_list = [
            {
                "key": "users",
                "query": User.objects.filter(
                    Q(name__icontains=q) | Q(email__iexact=q)
                ).exclude(pk=request.user.pk),
                "serializer_class": UserSearchResultsSerializer,
            },
            # {"places":"users", "query": Spot.objects.filter(Q(name__contains__iexact=q) | Q(city__iexact=q)),
            # "serializer_class":""}
        ]

        for querytype_dict in query_list:
            key = querytype_dict["key"]
            query = querytype_dict["query"]
            serializer_class = querytype_dict["serializer_class"]

            paginator = Paginator(query, initial_pagination)
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(default_page)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            data[key] = serializer_class(
                results.object_list, context={"request": request}, many=True
            ).data

        return Response(data=data)
