from rest_framework.response import Response
from rest_framework.generics import ListAPIView


class ListObjectAPIView(ListAPIView):
    """
    For when I want to return somehting like {"users":[]}
    insted of just []
    """

    key = None

    def get_model_name(self, many=False):
        if self.key:
            return self.key
        if many:
            model_name = str(self.serializer_class.Meta.model._meta.verbose_name_plural)
        else:
            model_name = self.serializer_class.Meta.model.__name__.lower()
        return model_name

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        model_name = self.get_model_name(many=True)
        return Response({model_name: serializer.data})
