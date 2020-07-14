from rest_framework.pagination import PageNumberPagination
from .result_handler import ResultGenerator


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return ResultGenerator.gen_success_result({
            'current': self.page.number,
            'total': self.page.paginator.count,
            'results': data
        })
