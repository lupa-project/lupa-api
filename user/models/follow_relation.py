from django.db import models

from utils.models import TimestampedModel


class FollowRelation(TimestampedModel):
    # - 이 친구가 이제 FollowRelation 모델입니다
    # - `UserA 가 UserB 를 팔로우하다` 대한 정의가 가능해야 합니다.
    # - User 모델은 `django.contrib.auth.models.User` 를 사용하시면 됩니다.
    # - 만들어지는 모델은 다음과 같은 표현이 가능해야합니다.
    #     - `UserA 는 UserB 를 팔로우하였으며, 아직 승인되지 않았다 / 승인되었다`

    class Meta:
        db_table = 'follow_relation'
        verbose_name = 'Follow Relation'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')
