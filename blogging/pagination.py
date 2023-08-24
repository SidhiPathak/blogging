"""
Django rest framework default pagination
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'nextPageNumber': self.page.next_page_number() if self.page.has_next() else None,
            'previousPageNumber': self.page.previous_page_number() if self.page.has_previous() else None,
            'next': self.get_next_link() if self.page.has_next() else None,
            'previous': self.get_previous_link() if self.page.has_previous() else None,
            'pages': self.page.paginator.num_pages,
            'results': data
        })