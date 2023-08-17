from django.db.models import (
    Model,
    DateTimeField
)
from datetime import datetime


class AbstractsDateTime(Model):
    """AbstractsDateTime"""

    created_at = DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True
    )
    updated_at = DateTimeField(
        verbose_name='Время обновления',
        auto_now=True,
    )
    deleted_at = DateTimeField(
        verbose_name='Время удаления',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def delete(self: 'AbstractsDateTime'):
        """Delete obj"""
        self.datetime_deleted: datetime = datetime.now()
        self.save(
            update_fields=['datetime']
        )