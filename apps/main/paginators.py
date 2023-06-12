from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 100000

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

    def get_limit(self, request):
        limit = request.query_params.get('limit')
        if limit:
            try:
                return int(limit)
            except ValueError:
                pass
        return self.page_size

    def get_offset(self, request):
        offset = request.query_params.get('offset')
        if offset:
            try:
                return int(offset)
            except ValueError:
                pass
        return 0

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_limit(request)
        self.offset = self.get_offset(request)
        return super().paginate_queryset(queryset, request, view)
