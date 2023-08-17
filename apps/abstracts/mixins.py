# Python
from typing import Any, Optional, Union

# Rest
from rest_framework.response import Response

# Apps
from abstracts.paginators import (
    AbstractPageNumberPaginator,
)


class ResponseMixin:
    """ResponseMixin."""

    def get_json_response(
        self,
        data: dict[Any, Any],
        paginator: AbstractPageNumberPaginator = None
    ) -> Response:

        if paginator:
            return paginator.get_paginated_response(
                data
            )
        return Response(
            {
                'results': data
            }
        )
