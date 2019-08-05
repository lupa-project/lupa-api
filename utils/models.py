from django.db import models


class TimestampedModel(models.Model):
    """생성,수정일시를 기록하는 필드를 포함한 모델
    """
    created_datetime = models.DateTimeField(
        verbose_name='생성일시',
        auto_now_add=True,
    )
    updated_datetime = models.DateTimeField(
        verbose_name='수정일시',
        auto_now=True,
    )

    class Meta:
        abstract = True
