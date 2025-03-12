from rest_framework.response import Response
from rest_framework import pagination


class PostPagination(pagination.PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total objects": self.page.paginator.count,
                "total pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
