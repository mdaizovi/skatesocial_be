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

# from .serializers import (
#     DualLogInSerializer,
# )

User = get_user_model()


class SearchView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    allowed_methods = ("GET",)

    def get(self, request, format=None):
        data = {}
        initial_pagination = 25
        default_page = 1

        # user = request.user
        q = request.GET.get("search")
        page = request.GET.get("page", default_page)

        for k, v in {
            "users": User.objects.filter(
                Q(name__contains__iexact=q) | Q(email__iexact=q)
            ),
            "places": Spot.objects.filter(
                Q(name__contains__iexact=q) | Q(city__iexact=q)
            ),
        }.items():
            paginator = Paginator(v, initial_pagination)
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(default_page)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            # do something with results and appropriate serializer.
            data[k] = results

        return Response(data=data)
