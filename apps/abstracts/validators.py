from typing import Optional

from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import APIException

from django.core.exceptions import ValidationError


class APIValidator(APIException):
    
    status_code: Optional[str] = None

    def __init__(
        self, detail: dict, field: str, code: str
    ) -> None:

        if code == '500':
            self.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        elif code == '404':
            self.status_code = HTTP_404_NOT_FOUND
        elif code == '403':
            self.status_code = HTTP_403_FORBIDDEN
        elif code == '400':
            self.status_code = HTTP_400_BAD_REQUEST
        else:
            raise ValidationError(
                'Статус код неизвестен'
            )

        if detail:
            self.detail = {
                field: detail
            }
        else:
            self.detail = {
                'error': 'Сервер не отвечает'
            }