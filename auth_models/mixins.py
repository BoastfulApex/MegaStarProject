"""
Basic building blocks for generic class based views.

We don't bind behaviour to http method handlers yet,
which allows mixin classes to be composed in interesting ways.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class CreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": serializer.data,
                 "message": []}, status=status.HTTP_200_OK, headers=headers
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": serializer.data,
                 "message": []}, status=status.HTTP_200_OK
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": serializer.data,
                 "message": []}, status=status.HTTP_200_OK
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateModelMixin:
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(
                {"status": True,
                 "code": 200,
                 "data": serializer.data,
                 "message": []}, status=status.HTTP_200_OK
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": []}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_destroy(self, instance):
        instance.delete()
